# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/16   9:37
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""
__all__ = ["Dice"]

import torch
from torch import Tensor

from .loss import BaseLoss


class Dice(BaseLoss):
    """

    Args:
        eps: The min divisor to smooth the computation of compensation factor. Default: ``1e-8``.
        name: Name of the loss function. Default: ``RMSE_loss``.
        loss_weight: Loss weight.  Default: ``1.0``.
    """
    def __init__(self,
                 eps: float = 1e-8,
                 name: str = "RMSE_loss",
                 loss_weight: float = 1.0,
                 ) -> None:
        reduction = "mean"
        super(Dice, self).__init__(name, reduction, loss_weight)
        self.eps = eps
    
    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        intersection = 2 * torch.sum(input * target) + self.eps
        union = torch.sum(input) + torch.sum(target)
        loss = 1 - intersection / union
        return self._reduce(loss, normalizer=1.0)
