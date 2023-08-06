# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/31   16:07
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["ChannelAtt"]

import torch
import torch.nn as nn


class ChannelAtt(nn.Module):
    def __init__(self, channels):
        super(ChannelAtt, self).__init__()
        self.channels = channels
        self.bn2 = nn.BatchNorm2d(self.channels, affine=True)


    def forward(self, x):
        residual = x
        x = self.bn2(x)
        weight_bn = self.bn2.weight.data.abs() / torch.sum(self.bn2.weight.data.abs())
        x = x.permute(0, 2, 3, 1).contiguous()
        x = torch.mul(weight_bn, x)
        x = x.permute(0, 3, 1, 2).contiguous()
        x = torch.sigmoid(x) * residual #
        return x