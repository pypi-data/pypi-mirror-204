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

__all__ = ["SAMConvLSTM", ]

from typing import Tuple

import torch
from torch import nn, Tensor


class ConvLSTM(nn.Module):
    """ConvLSTM
    
    """
    
    def __init__(self, in_channel: int,
                 out_channel: int,
                 kernel_size: int = 3,
                 stride: int = 1) -> None:
        super(ConvLSTM, self).__init__()
        padding = kernel_size // 2
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.forget_bias = 1.0
        # Convolutional Layers
        self.conv_x = nn.Sequential(nn.Conv2d(in_channel, out_channel * 4, kernel_size, stride=stride, padding=padding),
                                    nn.GroupNorm(num_groups=1, num_channels=out_channel * 4))
        self.conv_h = nn.Sequential(nn.Conv2d(out_channel, out_channel * 4, kernel_size, stride=stride,
                                              padding=padding),
                                    nn.GroupNorm(num_groups=1, num_channels=out_channel * 4))

    def forward(self, x: Tensor, h: Tensor, c: Tensor) -> Tuple[Tensor, Tensor]:
        # Self-Attention
        x_context = self.conv_x(x)
        h_context = self.conv_h(h)
    
        x_i, x_f, x_g, x_o = torch.split(x_context, self.out_channel, dim=1)
        h_i, h_f, h_g, h_o = torch.split(h_context, self.out_channel, dim=1)
    
        i = torch.sigmoid(x_i + h_i)
        f = torch.sigmoid(x_f + h_f + self.forget_bias)
        g = torch.tanh(x_g + h_g)
        o = torch.sigmoid(x_o + h_o)
    
        c_new = f * c + i * g
        h_new = o * torch.tanh(c_new)
        return h_new, c_new


class SAMConvLSTM(nn.Module):
    """Self-Attention Memory ConvLSTM

    References:
        [1] Lin Z, Li M, Zheng Z, et al. Self-Attention ConvLSTM for Spatiotemporal Prediction[J]. Proceedings of the
            AAAI Conference on Artificial Intelligence, 2020, 34(7):11531-11538.

    """
    
    def __init__(self, in_channel: int,
                 out_channel: int,
                 kernel_size: int = 3,
                 stride: int = 1) -> None:
        super(SAMConvLSTM, self).__init__()
        padding = kernel_size // 2
        self.in_channel = in_channel
        self.out_channel = out_channel
        self.forget_bias = 1.0
        # Convolutional LSTM
        self.convlstm = ConvLSTM(in_channel=in_channel, out_channel=out_channel, kernel_size=kernel_size, stride=stride)
        
        # Self-Attention Memory
        self.down_h = nn.Sequential(nn.Conv2d(out_channel, out_channel, (3, 3), stride=(2, 2), padding=1),
                                    nn.GroupNorm(16, out_channel),
                                    nn.LeakyReLU(0.2, inplace=True))
        self.down_m = nn.Sequential(nn.Conv2d(out_channel, out_channel, (3, 3), stride=(2, 2), padding=1),
                                    nn.GroupNorm(16, out_channel),
                                    nn.LeakyReLU(0.2, inplace=True))
        
        self.hidden_q = nn.Conv2d(out_channel, out_channel, (1, 1))
        self.hidden_k = nn.Conv2d(out_channel, out_channel, (1, 1))
        self.hidden_v = nn.Conv2d(out_channel, out_channel, (1, 1))
        
        self.memory_k = nn.Conv2d(out_channel, out_channel, (1, 1))
        self.memory_v = nn.Conv2d(out_channel, out_channel, (1, 1))
        
        self.conv_fusion = nn.Conv2d(out_channel * 2, out_channel, (1, 1))
        self.up_h = nn.Sequential(nn.ConvTranspose2d(out_channel, out_channel, (3, 3), stride=(2, 2),
                                                     padding=(1, 1), output_padding=(1, 1)),
                                  nn.GroupNorm(16, out_channel),
                                  nn.LeakyReLU(0.2, inplace=True))
        self.up_m = nn.Sequential(nn.ConvTranspose2d(out_channel, out_channel, (3, 3), stride=(2, 2),
                                                     padding=(1, 1), output_padding=(1, 1)),
                                  nn.GroupNorm(16, out_channel),
                                  nn.LeakyReLU(0.2, inplace=True))
        self.up_z = nn.Sequential(nn.ConvTranspose2d(out_channel, out_channel, (3, 3), stride=(2, 2),
                                                     padding=(1, 1), output_padding=(1, 1)),
                                  nn.GroupNorm(16, out_channel),
                                  nn.LeakyReLU(0.2, inplace=True))
        self.conv_h2h = nn.Sequential(nn.Conv2d(out_channel, out_channel * 3, (5, 5), stride=(1, 1),
                                                padding=2, bias=False),
                                      nn.GroupNorm(num_groups=1, num_channels=out_channel * 3))
        self.conv_z2h = nn.Sequential(nn.Conv2d(out_channel, out_channel * 3, (5, 5), stride=(1, 1),
                                                padding=2, bias=False),
                                      nn.GroupNorm(num_groups=1, num_channels=out_channel * 3))
        
        self.softmax = nn.Softmax(dim=-1)
    
    def sam(self, h: Tensor, m: Tensor) -> Tuple[Tensor, Tensor]:
        """Self-Attention Memory Block

        Args:
            h(torch.Tensor):
            m(torch.Tensor):

        """
        h = self.down_h(h)
        m = self.down_m(m)
        
        batch, channel, height, width = h.size()
        # Self Attention in hidden state
        # [N, ]
        hidden_q = self.hidden_q(h).view(batch, -1, height * width).permute(0, 2, 1)
        # [ ]
        hidden_k = self.hidden_k(h).view(batch, -1, height * width)
        # [ ]
        hidden_energy = torch.bmm(hidden_q, hidden_k)
        # [ ]
        hidden_attention = self.softmax(hidden_energy).permute(0, 2, 1)
        # [N, C, H*W]
        hidden_v = self.hidden_v(h).view(batch, -1, height * width)
        
        # [N, C, H, W]
        hidden_out = torch.bmm(hidden_v, hidden_attention).view(batch, channel, height, width)
        
        # Self Attention in memory state
        # [ ]
        memory_k = self.memory_k(m).view(batch, -1, height * width)
        # [ ]
        memory_energy = torch.bmm(hidden_q, memory_k)
        # [ ]
        memory_attention = self.softmax(memory_energy).permute(0, 2, 1)
        # [ ]
        memory_v = self.memory_v(m).view(batch, -1, height * width)
        
        # [N, C, H, W]
        memory_out = torch.bmm(memory_v, memory_attention).view(batch, channel, height, width)
        
        # Fusion
        z = self.conv_fusion(torch.cat([hidden_out, memory_out], dim=1))
        
        # Output
        z = self.up_z(z)
        h = self.up_h(h)
        m = self.up_m(m)
        
        h2h = self.conv_h2h(h)
        z2h = self.conv_z2h(z)
        
        i, g, o = torch.split(h2h + z2h, self.out_channel, dim=1)
        i = torch.sigmoid(i)
        g = torch.tanh(g)
        o = torch.sigmoid(o)
        
        m_new = i * g + (1 - i) * m
        h_new = o * m_new
        
        return h_new, m_new
    
    def forward(self, x: Tensor, h: Tensor, c: Tensor, m: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
        # ConvLSTM
        h_new, c_new = self.convlstm(x, h, c)
        # Self-Attention Memory
        h_new, m_new = self.sam(h_new, m)
        return h_new, c_new, m_new
