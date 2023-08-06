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

__all__ = ["SMU", "SMU1"]

import torch
from torch import nn, Tensor


class SMU(nn.Module):
    """
    Implementation of SMU activation.
    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    Parameters:
        - alpha: hyper parameter
    References:
        - See related paper:
        https://arxiv.org/abs/2111.04682
    Examples:
        >>> smu = SMU()
        >>> x = torch.Tensor([0.6,-0.3])
        >>> x = smu(x)
    """

    def __init__(self, alpha=0.25):
        """
        Initialization.
        INPUT:
            - alpha: hyper parameter
            aplha is initialized with zero value by default
        """
        super(SMU, self).__init__()
        self.alpha = alpha
        # initialize mu
        self.mu = torch.nn.Parameter(torch.tensor(1000000.0))

    def forward(self, x: Tensor) -> Tensor:
        return ((1 + self.alpha) * x + (1 - self.alpha) * x * torch.erf(self.mu * (1 - self.alpha) * x)) / 2


class SMU1(nn.Module):
    """
    Implementation of SMU-1 activation.
    Shape:
        - Input: (N, *) where * means, any number of additional
          dimensions
        - Output: (N, *), same shape as the input
    Parameters:
        - alpha: hyper parameter
    References:
        - See related paper:
        https://arxiv.org/abs/2111.04682
    Examples:
        >>> smu1 = SMU1()
        >>> x = torch.Tensor([0.6,-0.3])
        >>> x = smu1(x)
    """

    def __init__(self, alpha=0.25):
        """
        Initialization.
        INPUT:
            - alpha: hyper parameter
            aplha is initialized with zero value by default
        """
        super(SMU1, self).__init__()
        self.alpha = alpha
        # initialize mu
        self.mu = torch.nn.Parameter(torch.tensor(4.352665993287951e-9))

    def forward(self, x: Tensor) -> Tensor:
        return ((1 + self.alpha) * x + torch.sqrt(torch.square(x - self.alpha * x) + torch.square(self.mu))) / 2