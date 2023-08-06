# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/7   9:10
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["SeesawLoss"]


import torch
from torch import Tensor
import torch.nn.functional as F

from .loss import GeneralizedCrossEntropyLoss


class SeesawLoss(GeneralizedCrossEntropyLoss):
    """Implementation of seesaw loss.

    Notes:
        Refers to `Seesaw Loss for Long-Tailed Instance Segmentation (CVPR 2021)
        <https://arxiv.org/abs/2008.10032>

    Args:
        num_classes: The number of classes. Default: ``1000``.
        p: The ``p`` in the mitigation factor. Default: ``0.8``.
        q: The ``q`` in the compensation factor. Default: ``2.0``.
        eps: The min divisor to smooth the computation of compensation factor. Default: ``1e-2``.
        name: Name of the loss function. Default: ``See_saw_loss``.
        reduction: Reduction type, choice of mean, none, sum. Default: ``mean``.
        loss_weight: Loss weight.  Default: ``1.0``.
        ignore_index: The class index to be ignored. Default: ``-1``.
    """

    def __init__(self,
                 name: str = "generalized_cross_entropy_loss",
                 reduction: str = "mean",
                 loss_weight: float = 1.0,
                 ignore_index: int = -1,
                 num_classes: int = 1000,
                 p: float = 0.8,
                 q: float = 2.0,
                 eps: float = 1e-2
                 ) -> None:
        """

        """
        activation_type = "softmax"
        super().__init__(name, reduction, loss_weight, activation_type, ignore_index)
        self.num_classes = num_classes
        self.p = p
        self.q = q
        self.eps = eps

        # cumulative samples for each category
        self.register_buffer("accumulated", torch.zeros(self.num_classes, dtype=torch.float))

    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        if self.accumulated.device != input.device:
            self.accumulated = self.accumulated.cuda(input.device)

        input = self.flatten(input)
        target = torch.flatten(target)
        # accumulate the samples for each category
        for cls in range(self.num_classes):
            self.accumulated[cls] += torch.sum(target == cls)

        one_hot_target = F.one_hot(target, self.num_classes)
        seesaw_weights = input.new_ones(one_hot_target.size())

        # mitigation factor
        if self.p > 0:
            matrix = self.accumulated[None, :].clamp(min=1) / self.accumulated[:, None].clamp(min=1)
            index = (matrix < 1.0).float()
            sample_weights = matrix.pow(self.p) * index + (1 - index)
            mitigation_factor = sample_weights[target.long(), :]
            seesaw_weights = seesaw_weights * mitigation_factor

        # compensation factor
        if self.q > 0:
            scores = F.softmax(input.detach(), dim=1)
            self_scores = scores[torch.arange(0, len(scores)).to(scores.device).long(), target.long()]
            score_matrix = scores / self_scores[:, None].clamp(min=self.eps)
            index = (score_matrix > 1.0).float()
            compensation_factor = score_matrix.pow(self.q) * index + (1 - index)
            seesaw_weights = seesaw_weights * compensation_factor

        input = input + (seesaw_weights.log() * (1 - one_hot_target))
        loss = F.cross_entropy(input, target, ignore_index=self.ignore_index, reduction="none")
        return self._reduce(loss)
