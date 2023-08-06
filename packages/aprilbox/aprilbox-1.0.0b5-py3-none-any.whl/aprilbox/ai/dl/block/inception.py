# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/8   21:15
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["InceptionBlock", "InceptionModule"]

from typing import Callable

import torch
from torch import nn, Tensor


class InceptionModule(nn.Module):
    """
    InceptionModule.

    Args:
        input_len: Input tensor length.
        conv_out_size: Output length for conv and pooling layer.
        kernel_size: Kenel size for conv layers.
        activation: The activation function.
        use_bottleneck: If use bottleneck layer or not, Set to True by default.
    """

    def __init__(self,
                 input_len: int,
                 conv_out_size: int,
                 kernel_size: int = 40,
                 activation: Callable = nn.ReLU(),
                 use_bottleneck: bool = True):
        super().__init__()

        # compute kernel size
        kernel_size = [kernel_size // (2 ** i) for i in range(3)]
        kernel_size = [k if k % 2 != 0 else k - 1 for k in kernel_size]  # ensure odd ks
        # init bottleneck layer
        if (input_len > 1) and use_bottleneck:
            self.bottleneck = nn.Conv1d(input_len, conv_out_size, 1, bias=False)

            # init conv layers
            self.convs = nn.ModuleList([
                nn.Conv1d(conv_out_size, conv_out_size, k, bias=False, padding=k // 2) for k in kernel_size])

        else:
            self.bottleneck = None
            self.convs = nn.ModuleList([
                nn.Conv1d(input_len, conv_out_size, k, bias=False, padding=k // 2) for k in kernel_size])
        # init pooling layer
        self.maxconvpool = nn.Sequential(*[nn.MaxPool1d(3, stride=1, padding=1),
                                           nn.Conv1d(input_len, conv_out_size, 1, bias=False)])

        # init BN layer
        self.bn = nn.BatchNorm1d(conv_out_size * 4)
        self.act = activation

    def forward(self, x: Tensor) -> Tensor:
        """
        InceptionModule forward function.

        Args:
            x(paddle.Tensor): input data in format of paddle.Tensor.
        Returns:
            paddle.Tensor: The output of the InceptionModule.
        """

        input_tensor = x

        if self.bottleneck:
            x = self.bottleneck(input_tensor)

        x = torch.cat([conv(x) for conv in self.convs] + [self.maxconvpool(input_tensor)], dim=1)
        return self.act(self.bn(x))


class InceptionBlock(nn.Module):
    """
    InceptionBlock.

    Args:
        input_len: Input tensor length.
        output_len: Output tensor length.
        kernel_size: Kenel size for conv layers.
        depth: The depth of InceptionBlock.
        activation: The activation function.
        use_residual: If add residuals between Inception modules.
        use_bottleneck: If use bottleneck layer or not, Set to True by default.
    """

    def __init__(self,
                 input_len: int,
                 output_len: int = 128,
                 kernel_size: int = 40,
                 depth: int = 6,
                 activation: Callable = nn.ReLU(),
                 use_residual: bool = True,
                 use_bottleneck: bool = True):
        super().__init__()
        self.residual, self.depth = use_residual, depth
        self.inception, self.shortcut = nn.ModuleList(), nn.ModuleList()
        for d in range(depth):
            self.inception.append(
                InceptionModule(input_len if d == 0 else output_len, int(output_len / 4), kernel_size=kernel_size,
                                activation=activation, use_bottleneck=use_bottleneck))
            if self.residual and d % 3 == 2:
                n_in, n_out = input_len if d == 2 else output_len, output_len
                self.shortcut.append(nn.BatchNorm1d(n_in) if n_in == n_out else nn.Conv1d(n_in, n_out, 1))
        self.act = nn.ReLU()

    def forward(self, x):
        """
        forward function.

        Args:
            x(paddle.Tensor): input data in format of paddle.Tensor.
        Returns:
            paddle.Tensor: The output of the InceptionBlock.
        """
        res = x
        for d, l in enumerate(range(self.depth)):
            x = self.inception[d](x)
            if self.residual and d % 3 == 2: res = x = self.act(x.add(self.shortcut[d // 3](res)))
        return x