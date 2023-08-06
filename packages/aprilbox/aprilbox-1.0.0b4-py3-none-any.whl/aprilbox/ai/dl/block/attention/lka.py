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

__all__ = ["LKA", "LKABlock"]

import torch.nn as nn


class LKA(nn.Module):
    """Large Kernel Attention(LKA)

    Notes:
        Refers to `Visual attention network
        <https://arxiv.org/abs/2202.09741>
    """

    def __init__(self, in_channel: int):
        super(LKA, self).__init__()

        self.dw_conv = nn.Conv2d(in_channel, in_channel, kernel_size=5, padding=2, groups=in_channel)
        self.dw_d_conv = nn.Conv2d(in_channel, in_channel, kernel_size=7, stride=1, padding=9, dilation=3, groups=in_channel)
        self.conv = nn.Conv2d(in_channel, in_channel, kernel_size=1, stride=1)

    def forward(self, x):
        output = self.dw_conv(x)
        output = self.dw_d_conv(output)
        output = self.conv(output)
        return x * output


class LKABlock(nn.Module):
    def __init__(self, in_channel: int):
        super(LKABlock, self).__init__()
        self.base = nn.Sequential(nn.BatchNorm2d(in_channel),
                                  nn.Conv2d(in_channel, in_channel, 1, 1, bias=False),
                                  LKA(in_channel),
                                  nn.Conv2d(in_channel, in_channel, 1, 1, bias=False))

    def forward(self, x):
        output = self.base(x)
        return x + output