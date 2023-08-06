# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/31   19:53
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""


__all__ = ["BaseLoss", "GeneralizedCrossEntropyLoss"]

from abc import ABC
from typing import Optional

import torch
from torch import nn, Tensor


class BaseLoss(nn.Module):
    """

    Args:
        name: Name of the loss function. Default: ``base.py``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``none``.
        loss_weight: Loss weight.  Default: ``1.0``.
    """
    def __init__(self,
                 name: str = "base.py",
                 reduction: str = "none",
                 loss_weight: float = 1.0
                 ) -> None:
        super(BaseLoss, self).__init__()
        self.name = name
        self.reduction = reduction
        self.loss_weight = loss_weight

    def _reduce(self, loss: Tensor, **kwargs) -> Tensor:
        if self.reduction == "none":
            ret = loss * self.loss_weight
        elif self.reduction == "mean":
            normalizer = kwargs.get("normalizer", loss.numel())
            ret = loss.sum() / normalizer * self.loss_weight
        elif self.reduction == "sum":
            ret = loss.sum() * self.loss_weight
        else:
            raise ValueError(self.reduction + " is not valid")
        return ret

    def forward(self,
                input: Tensor,
                target: Tensor,
                normalizer: Optional[int] = None,
                **kwargs
                ) -> Tensor:
        raise NotImplementedError



class GeneralizedCrossEntropyLoss(BaseLoss, ABC):
    """

    Args:
        name: Name of the loss function. Default: ``generalized_cross_entropy_loss``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``none``.
        loss_weight: Loss weight.  Default: ``1.0``.
        activation_type: The activation method. Default: ``Softmax``.
        ignore_index: The class index to be ignored. Default: ``-1``.
    """
    def __init__(self,
                 name: str = "generalized_cross_entropy_loss",
                 reduction: str = "none",
                 loss_weight: float = 1.0,
                 activation_type: str = "softmax",
                 ignore_index: int = -1
                 ) -> None:
        BaseLoss.__init__(self,
                          name=name,
                          reduction=reduction,
                          loss_weight=loss_weight)
        self.activation_type = activation_type
        self.ignore_index = ignore_index

    @staticmethod
    def flatten(x: Tensor, dim: int = 1) -> Tensor:
        if x.dim() > 2:
            # shape like B * Num_class * ...
            return torch.flatten(torch.flatten(x, start_dim=dim + 1, end_dim=-1).permute(0, 2, 1), start_dim=0, end_dim=1)
        elif x.dim() == 2:
            # shape like N * Num_class
            return x
        else:
            # shape is not supported
            raise ValueError("CrossEntropyLoss is expected input N-dims input.")
