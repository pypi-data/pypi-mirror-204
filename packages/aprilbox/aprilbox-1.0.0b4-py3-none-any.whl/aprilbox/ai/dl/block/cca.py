# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/31   15:57
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["CCA"]

import torch
from torch import nn, Tensor
import torch.nn.functional as F

from ..activation import SMU


class CCA(nn.Module):
    """
    CCA Block
    """
    def __init__(self, fg, fx):
        super().__init__()
        self.mlp_x = nn.Linear(fx, fx)
        self.mlp_g = nn.Linear(fg, fx)
        self.atc = SMU()

    def forward(self, g: Tensor, x: Tensor) -> Tensor:
        # channel-wise attention
        avg_pool_x = F.avg_pool2d(x, (x.size(2), x.size(3)), stride=(x.size(2), x.size(3)))
        channel_att_x = self.mlp_x(avg_pool_x.view(x.size(0), -1))
        avg_pool_g = F.avg_pool2d(g, (g.size(2), g.size(3)), stride=(g.size(2), g.size(3)))
        channel_att_g = self.mlp_g(avg_pool_g.view(x.size(0), -1))
        channel_att_sum = (channel_att_x + channel_att_g)/2.0
        scale = torch.sigmoid(channel_att_sum).unsqueeze(2).unsqueeze(3).expand_as(x)
        x_after_channel = x * scale
        out = self.atc(x_after_channel)
        return out