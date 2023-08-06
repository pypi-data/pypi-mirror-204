# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:32
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["SSIM"]

import torch
from torch import nn, Tensor
import torch.nn.functional as F
from torch.autograd import Variable

from .loss import BaseLoss


def gaussian(window_size: int, sigma: float) -> Tensor:
    gauss = Tensor([torch.exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2)) for x in range(window_size)])
    return gauss / gauss.sum()


def create_window(window_size: int, channel: int) -> Variable:
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())
    return window


class SSIM(BaseLoss):
    """
    
    Args:
        channel:
        window_size: default ``11``.
        size_average: default ``True``.
        one_minus: default ``False``.
        name: Name of the loss function. Default: ``SSIM_loss``.
        loss_weight: Loss weight.  Default: ``1.0``.
    References:
        Unknown
    """
    def __init__(self,
                 channel: int = 1,
                 window_size: int = 11,
                 size_average: bool = True,
                 one_minus: bool = False,
                 name: str = "SSIM_loss",
                 loss_weight: float = 1.0,
                 ) -> None:
        reduction = "mean"
        super(SSIM, self).__init__(name, reduction, loss_weight)
        self.channel = channel
        self.window_size = window_size
        self.size_average = size_average
        self.one_minus = one_minus
        self.window = create_window(window_size, self.channel)

    def _ssim(self, img1: torch.Tensor, img2: torch.Tensor) -> torch.Tensor:
        mu1 = F.conv2d(img1, self.window, padding=self.window_size // 2, groups=self.channel)
        mu2 = F.conv2d(img2, self.window, padding=self.window_size // 2, groups=self.channel)

        mu1_sq, mu2_sq = mu1.pow(2), mu2.pow(2)
        mu1_mu2 = mu1 * mu2

        sigma1_sq = F.conv2d(img1 * img1, self.window, padding=self.window_size // 2, groups=self.channel) - mu1_sq
        sigma2_sq = F.conv2d(img2 * img2, self.window, padding=self.window_size // 2, groups=self.channel) - mu2_sq
        sigma12 = F.conv2d(img1 * img2, self.window, padding=self.window_size // 2, groups=self.channel) - mu1_mu2

        C1, C2 = 0.01 ** 2, 0.03 ** 2
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
        if self.size_average:
            return ssim_map.mean()
        else:
            return ssim_map.mean(1).mean(1).mean(1)

    def calc_ssim(self, img1, img2):
        if self.one_minus:
            return 1 - self._ssim(img1, img2)
        else:
            return self._ssim(img1, img2)

    def forward(self, input: Tensor, target: Tensor, **kwargs) -> Tensor:
        input = torch.flatten(input, start_dim=0, end_dim=-3)
        target = torch.flatten(target, start_dim=0, end_dim=-3)

        if input.shape[-3] == self.channel and self.window.data.type() == input.data.type():
            window = self.window
        else:
            window = create_window(self.window_size, input.shape[-3])

        if input.is_cuda:
            window = window.cuda(input.get_device())
        window = window.type_as(input)

        self.window = window
        self.channel = input.shape[-3]
        loss = self.calc_ssim(input, target)
        return self._reduce(loss, normalizer=1.0)
