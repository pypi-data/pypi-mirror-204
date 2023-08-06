import math

import torch
from torch.optim.optimizer import Optimizer

from pytorch_optimizer.base.exception import NoSparseGradientError
from pytorch_optimizer.base.optimizer import BaseOptimizer
from pytorch_optimizer.base.types import BETAS, CLOSURE, DEFAULTS, LOSS, PARAMETERS


class AdaBelief(Optimizer, BaseOptimizer):
    r"""Adapting Step-sizes by the Belief in Observed Gradients.

    :param params: PARAMETERS. iterable of parameters to optimize or dicts defining parameter groups.
    :param lr: float. learning rate.
    :param betas: BETAS. coefficients used for computing running averages of gradient and the squared hessian trace.
    :param weight_decay: float. weight decay (L2 penalty).
    :param n_sma_threshold: number of SMA threshold (recommended is 5).
    :param weight_decouple: bool. the optimizer uses decoupled weight decay as in AdamW.
    :param fixed_decay: bool. fix weight decay.
    :param rectify: bool. perform the rectified update similar to RAdam.
    :param degenerated_to_sgd: bool. perform SGD update when variance of gradient is high.
    :param amsgrad: bool. whether to use the AMSBound variant.
    :param adamd_debias_term: bool. Only correct the denominator to avoid inflating step sizes early in training.
    :param eps: float. term added to the denominator to improve numerical stability.
    """

    def __init__(
        self,
        params: PARAMETERS,
        lr: float = 1e-3,
        betas: BETAS = (0.9, 0.999),
        weight_decay: float = 0.0,
        n_sma_threshold: int = 5,
        weight_decouple: bool = True,
        fixed_decay: bool = False,
        rectify: bool = True,
        degenerated_to_sgd: bool = True,
        amsgrad: bool = False,
        adamd_debias_term: bool = False,
        eps: float = 1e-16,
    ):
        self.lr = lr
        self.betas = betas
        self.weight_decay = weight_decay
        self.n_sma_threshold = n_sma_threshold
        self.weight_decouple = weight_decouple
        self.fixed_decay = fixed_decay
        self.rectify = rectify
        self.degenerated_to_sgd = degenerated_to_sgd
        self.adamd_debias_term = adamd_debias_term
        self.eps = eps

        self.validate_parameters()

        defaults: DEFAULTS = {
            'lr': lr,
            'betas': betas,
            'eps': eps,
            'weight_decay': weight_decay,
            'amsgrad': amsgrad,
            'adamd_debias_term': adamd_debias_term,
            'buffer': [[None, None, None] for _ in range(10)],
        }
        super().__init__(params, defaults)

    def validate_parameters(self):
        self.validate_learning_rate(self.lr)
        self.validate_betas(self.betas)
        self.validate_weight_decay(self.weight_decay)
        self.validate_epsilon(self.eps)

    def __str__(self) -> str:
        return 'AdaBelief'

    @torch.no_grad()
    def reset(self):
        for group in self.param_groups:
            for p in group['params']:
                state = self.state[p]

                state['step'] = 0
                state['exp_avg'] = torch.zeros_like(p)
                state['exp_avg_var'] = torch.zeros_like(p)
                if group['amsgrad']:
                    state['max_exp_avg_var'] = torch.zeros_like(p)

    @torch.no_grad()
    def step(self, closure: CLOSURE = None) -> LOSS:
        loss: LOSS = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            beta1, beta2 = group['betas']
            weight_decay: float = group['weight_decay']

            if self.rectify:
                n_sma_max: float = 2.0 / (1.0 - beta2) - 1.0

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                if grad.is_sparse:
                    raise NoSparseGradientError(str(self))

                state = self.state[p]
                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p)
                    state['exp_avg_var'] = torch.zeros_like(p)
                    if group['amsgrad']:
                        state['max_exp_avg_var'] = torch.zeros_like(p)

                if self.weight_decouple:
                    p.mul_(1.0 - (group['lr'] * weight_decay if not self.fixed_decay else weight_decay))
                elif weight_decay > 0.0:
                    grad.add_(p, alpha=weight_decay)

                state['step'] += 1
                exp_avg, exp_avg_var = state['exp_avg'], state['exp_avg_var']

                bias_correction1 = 1.0 - beta1 ** state['step']
                bias_correction2_sq = math.sqrt(1.0 - beta2 ** state['step'])

                exp_avg.mul_(beta1).add_(grad, alpha=1.0 - beta1)
                grad_residual = grad - exp_avg
                exp_avg_var.mul_(beta2).addcmul_(grad_residual, grad_residual, value=1.0 - beta2).add_(group['eps'])

                if group['amsgrad']:
                    max_exp_avg_var = state['max_exp_avg_var']
                    torch.max(max_exp_avg_var, exp_avg_var, out=max_exp_avg_var)
                    de_nom = max_exp_avg_var.sqrt()
                else:
                    de_nom = exp_avg_var.sqrt()
                de_nom.div_(bias_correction2_sq).add_(group['eps'])

                if not self.rectify:
                    step_size: float = group['lr'] if group['adamd_debias_term'] else group['lr'] / bias_correction1
                    p.addcdiv_(exp_avg, de_nom, value=-step_size)
                    continue

                buffered = group['buffer'][state['step'] % 10]
                if state['step'] == buffered[0]:
                    n_sma, step_size = buffered[1], buffered[2]
                else:
                    buffered[0] = state['step']
                    beta2_t = beta2 ** state['step']
                    n_sma = n_sma_max - 2 * state['step'] * beta2_t / (1 - beta2_t)
                    buffered[1] = n_sma

                    if n_sma >= self.n_sma_threshold:
                        step_size = math.sqrt(
                            (1 - beta2_t)
                            * (n_sma - 4)
                            / (n_sma_max - 4)
                            * (n_sma - 2)
                            / n_sma
                            * n_sma_max
                            / (n_sma_max - 2)
                        )
                        if not group['adamd_debias_term']:
                            step_size /= bias_correction1
                    elif self.degenerated_to_sgd:
                        step_size = 1.0 / bias_correction1
                    else:
                        step_size = -1

                    buffered[2] = step_size

                if n_sma >= self.n_sma_threshold:
                    de_nom = exp_avg_var.sqrt().add_(group['eps'])
                    p.addcdiv_(exp_avg, de_nom, value=-step_size * group['lr'])
                elif step_size > 0:
                    p.add_(exp_avg, alpha=-step_size * group['lr'])

        return loss
