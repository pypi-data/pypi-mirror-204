# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/20   13:44
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["FocalLoss", "EFocalLoss"]

from abc import ABC

import torch
from torch import nn, Tensor
import torch.nn.functional as F
from .loss import GeneralizedCrossEntropyLoss


class FocalLoss(GeneralizedCrossEntropyLoss, ABC):
    """Focal Loss

    Notes:
        Refers to `Focal Loss for Dense Object Detection
        <https://arxiv.org/abs/1708.02002>

    Args:
        num_classes: The number of classes. Default: ``1000``.
        alpha: Default: ``0.25``.
        gamma: Default: ``2.0``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``none``.
        loss_weight: Loss weight.  Default: ``1.0``.
        ignore_index: The class index to be ignored. Default: ``-1``.
    """
    def __init__(self,
                 num_classes: int = 1000,
                 alpha: float = 0.25,
                 gamma: float = 2.0,
                 reduction: str = "mean",
                 loss_weight: float = 1.0,
                 ignore_index: int = -1,
                 ) -> None:
        name = "focal_loss"
        activation_type = "softmax"
        GeneralizedCrossEntropyLoss.__init__(self,
                                             name=name,
                                             reduction=reduction,
                                             loss_weight=loss_weight,
                                             activation_type=activation_type,
                                             ignore_index=ignore_index)

        # cfg for focal loss
        self.gamma = gamma
        self.alpha = alpha

        # number of classes
        self.num_classes = num_classes


    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        # Flatten input & target
        input = self.flatten(input)
        target = torch.flatten(target)

        # One-hot target & ignore index
        target_one_hot = F.one_hot(target, num_classes=self.num_classes)
        sample_mask = torch.where(target != self.ignore_index, True, False)
        input = input[sample_mask]
        target = target_one_hot[sample_mask]

        pred = torch.sigmoid(input)
        pt = pred * target + (1 - pred) * (1 - target)
        ce = -1.0 * torch.log(pt)

        pt = torch.exp(-ce)
        focal_loss = self.alpha * torch.pow((1 - pt), self.gamma) * ce
        return self._reduce(focal_loss)


class EFocalLoss(GeneralizedCrossEntropyLoss, ABC):
    """Equalized Focal Loss

    Notes:
        Refers to `Equalized Focal Loss for Dense Long-Tailed Object Detection (CVPR 2022)
        <https://arxiv.org/abs/2201.02593v2>

        Refers to `Equalization Loss v2: A New Gradient Balance Approach for Long-tailed Object Detection
        <https://arxiv.org/abs/2012.08548>

    Args:
        num_classes: The number of classes. Default: ``1000``.
        alpha: Default: ``0.25``.
        gamma: Default: ``2.0``.
        factor: Default: ``8.0``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``none``.
        loss_weight: Loss weight.  Default: ``1.0``.
        ignore_index: The class index to be ignored. Default: ``-1``.
    """
    def __init__(self,
                 num_classes: int = 1000,
                 alpha: float = 0.25,
                 gamma: float = 2.0,
                 factor: float = 8.0,
                 reduction: str = "mean",
                 loss_weight: float = 1.0,
                 ignore_index: int = -1,
                 ) -> None:
        name = "equalized_focal_loss"
        activation_type = "sigmoid"
        GeneralizedCrossEntropyLoss.__init__(self,
                                             name=name,
                                             reduction=reduction,
                                             loss_weight=loss_weight,
                                             activation_type=activation_type,
                                             ignore_index=ignore_index)

        # cfg for focal loss
        self.gamma = gamma
        self.alpha = alpha
        self.factor = factor

        # ignore bg class and ignore idx
        self.num_classes = num_classes

        # initial variables
        self.pos_grad = torch.zeros(self.num_classes, requires_grad=False)
        self.neg_grad = torch.zeros(self.num_classes, requires_grad=False)
        self.pos_neg = torch.ones(self.num_classes, requires_grad=False)

    def collect_grad(self, input: Tensor, target: Tensor) -> None:
        # Gradient Guided Reweighing
        # prob = torch.sigmoid(input)
        grad = target * (1 - input) + target * (input - 1)
        grad = torch.abs(grad)

        pos_grad = torch.sum(grad * target, dim=0)
        neg_grad = torch.sum(grad * (1 - target), dim=0)

        self.pos_grad = self.pos_grad + pos_grad
        self.neg_grad = self.neg_grad + neg_grad
        self.pos_neg = torch.clamp(self.pos_grad / (self.neg_grad + 1e-10), min=0.0, max=1.0)

    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        # Flatten input & target
        input = self.flatten(input)
        target = torch.flatten(target)

        n, c = input.shape

        # One-hot target & ignore index
        target_one_hot = F.one_hot(target, num_classes=self.num_classes)
        sample_mask = torch.where(target != self.ignore_index, True, False)
        input = input[sample_mask]
        target = target_one_hot[sample_mask]

        # focusing factor
        dy_gamma = self.gamma + self.factor * (1 - self.pos_neg.detach())
        dy_gamma = dy_gamma.cuda(input.device)
        ff = dy_gamma.view(1, -1).expand(n, c)[sample_mask]
        # weight factor
        wf = ff / self.gamma

        pred = torch.sigmoid(input)
        pt = pred * target + (1 - pred) * (1 - target)
        ce = -1.0 * torch.log(pt + 1e-8)

        equalized_focal_loss = self.alpha * wf * torch.pow((1 - pt), ff) * ce
        # Collect gradient
        self.collect_grad(input=input, target=target)
        return self._reduce(equalized_focal_loss)