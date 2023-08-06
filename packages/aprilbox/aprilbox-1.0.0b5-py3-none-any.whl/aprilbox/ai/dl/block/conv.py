# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/29   17:29
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["BaseConvXNAct", "ConvGNReLU", "ConvBNReLU"]

from typing import Optional

from torch import nn, Tensor


class BaseConvXNAct(nn.Module):
    """Conv2d & Normalization & Action

    """
    def __init__(self,
                 in_channel: int,
                 out_channel: Optional[int] = None,
                 kernel_size: int = 3,
                 stride: int = 1,
                 padding: int = 0,
                 transpose: bool = False,
                 act_norm: bool = False,
                 **kwargs,
                 ) -> None:
        super(BaseConvXNAct, self).__init__()
        self.act_norm = act_norm

        norm = kwargs.pop("norm", "bn")
        act = kwargs.pop("act", "relu")

        # Conv Layer
        if transpose:
            self.conv = nn.ConvTranspose2d(in_channel, out_channel, kernel_size, stride=stride,
                                           padding=padding, output_padding=stride // 2, bias=~act_norm)
        else:
            self.conv = nn.Conv2d(in_channel, out_channel, kernel_size, stride=stride, padding=padding, bias=~act_norm)

        #  Normalize Layer & Action Layer
        if act_norm:
            if norm == "bn":
                self.norm = nn.BatchNorm2d(out_channel)
            elif norm == "gn":
                self.norm = nn.GroupNorm(kwargs.get("num_groups", 32), out_channel)
            else:
                raise NotImplemented

            if act == "relu":
                self.act = nn.ReLU(inplace=True)
            elif act == "leaky":
                self.act = nn.LeakyReLU(kwargs.get("negative_slope", 0.05), inplace=True)
            elif act == "silu":
                self.act = nn.SiLU(inplace=True)
            else:
                raise NotImplemented


    def forward(self, x: Tensor) -> Tensor:
        y = self.conv(x)
        if self.act_norm:
            y = self.act(self.norm(y))
        return y



class ConvBNReLU(BaseConvXNAct):
    """Conv2d & BatchNorm & Relu
    """
    def __init__(self,
                 in_channel: int,
                 out_channel: Optional[int] = None,
                 kernel_size: int = 3,
                 stride: int = 1,
                 padding: int = 0,
                 **kwargs,
                 ) -> None:
        kwargs.update({"norm": "bn", "act": "relu", "act_norm": True})
        super(ConvBNReLU, self).__init__(in_channel, out_channel, kernel_size, stride, padding, **kwargs)


class ConvGNReLU(BaseConvXNAct):
    """Conv2d & GroupNorm & Relu

    """
    def __init__(self,
                 in_channel: int,
                 out_channel: Optional[int] = None,
                 kernel_size: int = 3,
                 stride: int = 1,
                 padding: int = 0,
                 num_groups: int = 32,
                 **kwargs,
                 ) -> None:
        kwargs.update({"norm": "gn", "num_groups": num_groups, "act": "relu", "act_norm": True})
        super(ConvGNReLU, self).__init__(in_channel, out_channel, kernel_size, stride, padding, **kwargs)
