# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/25   11:26
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["TSLoss"]


import torch
from torch import Tensor

from .loss import BaseLoss


class TSLoss(BaseLoss):
    """

    Args:
        threshold: The threshold for classify. Default: ``0.1``.
        name: Name of the loss function. Default: ``TSLoss``.
        loss_weight: Loss weight.  Default: ``1.0``.
    """
    def __init__(self,
                 threshold: float = 0.1,
                 name: str = "TSLoss",
                 loss_weight: float = 1.0
                 ) -> None:
        reduction = "mean"
        super(TSLoss, self).__init__(name, reduction, loss_weight)
        self.threshold = threshold

    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        input_binary = (input >= self.threshold).float()
        target_binary = (target >= self.threshold).float()

        hits = torch.sum(input_binary * target_binary)
        misses = torch.sum((1 - input_binary) * target_binary)
        false_alarms = torch.sum(input_binary * (1 - target_binary))

        ts_loss = 1 - (hits + 1e-8) / (hits + misses + false_alarms + 1e-8)

        return self._reduce(ts_loss, normalizer=1.0)
