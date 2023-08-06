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

__all__ = ["UNet3D",]

import torch
from torch import nn, Tensor


class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()

    def forward(self):
        pass


class UNet3D(nn.Module):
    def __init__(self, in_channel: int,
                 out_channel: int
                 ) -> None:
        super(UNet3D, self).__init__()
        self.ec0 = self.encoder(in_channel, 32, bias=False, bn=False)
        self.ec1 = self.encoder(32, 64, bias=False, bn=False)
        self.ec2 = self.encoder(64, 64, bias=False, bn=False)
        self.ec3 = self.encoder(64, 128, bias=False, bn=False)
        self.ec4 = self.encoder(128, 128, bias=False, bn=False)
        self.ec5 = self.encoder(128, 256, bias=False, bn=False)
        self.ec6 = self.encoder(256, 256, bias=False, bn=False)
        self.ec7 = self.encoder(256, 512, bias=False, bn=False)

        self.pool0 = nn.MaxPool3d(2)
        self.pool1 = nn.MaxPool3d(2)
        self.pool2 = nn.MaxPool3d(2)

        self.dc9 = self.decoder(512, 512, kernel_size=2, stride=2, bias=False)
        self.dc8 = self.decoder(256 + 512, 256, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc7 = self.decoder(256, 256, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc6 = self.decoder(256, 256, kernel_size=2, stride=2, bias=False)
        self.dc5 = self.decoder(128 + 256, 128, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc4 = self.decoder(128, 128, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc3 = self.decoder(128, 128, kernel_size=2, stride=2, bias=False)
        self.dc2 = self.decoder(64 + 128, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc1 = self.decoder(64, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.dc0 = self.decoder(64, out_channel, kernel_size=1, stride=1, bias=False)

    def encoder(self, in_channel: int, out_channel: int, kernel_size: int = 3, stride: int = 1, padding: int = 0,
                bias: bool = True, bn: bool = False):
        if bn:
            layer = nn.Sequential(nn.Conv3d(in_channel, out_channel, kernel_size,
                                            stride=stride, padding=padding, bias=bias),
                                  nn.BatchNorm3d(out_channel),
                                  nn.ReLU())
        else:
            layer = nn.Sequential(nn.Conv3d(in_channel, out_channel, kernel_size,
                                            stride=stride, padding=padding, bias=bias),
                                  nn.ReLU())
        return layer

    def decoder(self,  in_channel: int, out_channel: int, kernel_size: int, stride: int = 1, padding: int = 0,
                output_padding: int = 0, bias: bool = True):
        layer = nn.Sequential(nn.ConvTranspose3d(in_channel, out_channel, kernel_size, stride=stride,
                               padding=padding, output_padding=output_padding, bias=bias),
                              nn.ReLU())
        return layer

    def forward(self, x: Tensor) -> Tensor:
        e0 = self.ec0(x)
        syn0 = self.ec1(e0)
        e1 = self.pool0(syn0)
        e2 = self.ec2(e1)
        syn1 = self.ec3(e2)
        del e0, e1, e2

        e3 = self.pool1(syn1)
        e4 = self.ec4(e3)
        syn2 = self.ec5(e4)
        del e3, e4

        e5 = self.pool2(syn2)
        e6 = self.ec6(e5)
        e7 = self.ec7(e6)
        del e5, e6

        d9 = torch.cat((self.dc9(e7), syn2))
        del e7, syn2

        d8 = self.dc8(d9)
        d7 = self.dc7(d8)
        del d9, d8

        d6 = torch.cat((self.dc6(d7), syn1))
        del d7, syn1

        d5 = self.dc5(d6)
        d4 = self.dc4(d5)
        del d6, d5

        d3 = torch.cat((self.dc3(d4), syn0))
        del d4, syn0

        d2 = self.dc2(d3)
        d1 = self.dc1(d2)
        del d3, d2

        d0 = self.dc0(d1)
        return d0
