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

__all__ = ["SplAttConv2d"]


import torch
import torch.nn as nn
import torch.nn.functional as F

from ...activation import MetaAconC


class RSoftMax(nn.Module):
    """
    
    Args:
        radix:
        cardinality:
    
    References:
        Unknown
    """
    def __init__(self, radix: int,
                 cardinality: int) -> None:
        super().__init__()
        self.radix = radix
        self.cardinality = cardinality

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch = x.size(0)
        if self.radix > 1:
            x = x.view(batch, self.cardinality, self.radix, -1).transpose(1, 2)
            x = F.softmax(x, dim=1)
            x = x.reshape(batch, -1)
        else:
            x = torch.sigmoid(x)
        return x

class SplAttConv2d(nn.Module):
    """Split-Attention Conv2d
    
    Args:
        in_channel:
        out_channel:
        kernel_size:
        stride: default `1`.
        padding: default `0`.
        dilation: default `1`.
        cardinality: default `1`.
        bias: default `True`.
        radix: default `2`.
        reduction_factor: default `4`.
        
    References:
        Unknown
    """
    
    def __init__(self, in_channel: int,
                 out_channel: int,
                 kernel_size: int,
                 stride: int = 1,
                 padding: int = 0,
                 dilation: int = 1,
                 cardinality: int = 1,
                 bias: bool = True,
                 radix: int = 2,
                 reduction_factor: int = 4) -> None:
        super(SplAttConv2d, self).__init__()
        inner_channel = max(in_channel * radix // reduction_factor, 32)
        self.radix = radix
        
        kernel_size = (kernel_size, kernel_size)
        stride = (stride, stride)
        padding = (padding, padding)
        dilation = (dilation, dilation)
        
        self.step1 = nn.Sequential(nn.Conv2d(in_channel, out_channel * radix, kernel_size=kernel_size, stride=stride,
                                             padding=padding, dilation=dilation, groups=cardinality * radix, bias=bias),
                                   nn.BatchNorm2d(out_channel * radix),
                                   MetaAconC(out_channel * radix))
        self.step2 = nn.Sequential(nn.Conv2d(out_channel, inner_channel, kernel_size=(1, 1), groups=cardinality),
                                   nn.BatchNorm2d(inner_channel),
                                   MetaAconC(inner_channel))
        self.step3 = nn.Conv2d(inner_channel, out_channel * radix, kernel_size=(1, 1), groups=cardinality)
        self.drop = nn.Dropout(0.5)
        self.softmax = RSoftMax(radix, cardinality)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.step1(x)
        
        batch, channel = x.shape[:2]
        split_x = torch.split(x, channel // self.radix, dim=1)
        if self.radix > 1:
            gap = sum(split_x)
        else:
            # todo 是否存在浅拷贝
            gap = x.clone()
        
        gap = self.step2(F.adaptive_avg_pool2d(gap, 1))
        
        attention = self.softmax(self.step3(gap)).view(batch, -1, 1, 1)
        if self.radix > 1:
            attentions = torch.split(attention, channel // self.radix, dim=1)
            out = sum([att * split for (att, split) in zip(attentions, split_x)])
        else:
            out = attention * x
        return out.contiguous()
