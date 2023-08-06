# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/08   17:53
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["RMSELoss"]

import torch
from torch import Tensor

from .loss import BaseLoss


class RMSELoss(BaseLoss):
    """RMSE loss function of predictions.

    References:
        [1] Deep learning prediction of incoming rainfalls: An operational service for the city of Beijing China.
        <https://ieeexplore.ieee.org/abstract/document/8955589>

    Args:
        p: The ``p`` argument for calculating. Default: ``6.0``.
        q: The ``q`` argument for calculating. Default: ``0.8``.
        name: Name of the loss function. Default: ``RMSE_loss``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``none``.
        loss_weight: Loss weight.  Default: ``1.0``.
    """
    def __init__(self,
                 p: float = 6.0,
                 q: float = 0.8,
                 name: str = "RMSE_loss",
                 reduction: str = "none",
                 loss_weight: float = 1.0
                 ) -> None:
        super(RMSELoss, self).__init__(name, reduction, loss_weight)
        self.p = p
        self.q = q

    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        loss = ((target - input) ** 2) * (torch.exp(target * self.p - self.q))
        return self._reduce(loss, **kwargs)
