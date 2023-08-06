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

__all__ = ["ResNet"]


import torch
from torch import nn, Tensor

from ..block.attention import SplAttConv2d
from ..activation import MetaAconC


class ResNet(nn.Module):
    """ResNet with Bottleneck Layer
    
    todo: fill the args docstring
    Args:
        in_channel:
        out_channel:
        width:
        stride:
        cardinality:
        dilation:
        radix:
    
    Notes:
        radix True:
            step1[conv1 --> bn1 --> MetaAconC1] -->
            step2[SplAtConv2d --> MetaAconC2] -->
            step3[conv3 --> bn3 --> shor cut --> MetaAconC3]
        radix False:
            step1[conv1 --> bn1 --> MetaAconC1] -->
            step2[conv2 --> bn2 --> MetaAconC2] -->
            step3[conv3 --> bn3 --> shor cut --> MetaAconC3]
    """
    
    def __init__(self, in_channel: int,
                 out_channel: int or None = None,
                 width: int = 64,
                 stride: int = 1,
                 cardinality: int = 1,
                 dilation: int = 1,
                 radix: int = 1) -> None:
        super(ResNet, self).__init__()
        inner_channel = int(out_channel * (width / 64)) * cardinality
        
        self.step1 = nn.Sequential(nn.Conv2d(in_channel, inner_channel, kernel_size=(1, 1), bias=False),
                                   nn.BatchNorm2d(inner_channel),
                                   MetaAconC(inner_channel))
        if radix >= 1:
            self.step2 = nn.Sequential(SplAttConv2d(inner_channel, inner_channel, kernel_size=3, stride=stride,
                                                    padding=dilation, dilation=dilation, cardinality=cardinality,
                                                    bias=False, radix=radix),
                                       MetaAconC(inner_channel))
        else:
            self.step2 = nn.Sequential(nn.Conv2d(inner_channel, inner_channel, kernel_size=(1, 1), bias=False),
                                       nn.BatchNorm2d(inner_channel),
                                       MetaAconC(inner_channel))
        self.step3 = nn.Sequential(nn.Conv2d(inner_channel, out_channel, kernel_size=(1, 1), bias=False),
                                   nn.BatchNorm2d(out_channel))
        
        self.shortcut = nn.Sequential(nn.Conv2d(in_channel, out_channel, kernel_size=(1, 1), stride=(stride, stride),
                                                bias=False),
                                      nn.BatchNorm2d(out_channel))
        
        self.out_action = MetaAconC(out_channel)
    
    def forward(self, x: Tensor) -> Tensor:
        residual = x
        out = self.step1(x)
        out = self.step2(out)
        out = self.step3(out)
        out += self.shortcut(residual)
        out = self.out_action(out)
        return out
