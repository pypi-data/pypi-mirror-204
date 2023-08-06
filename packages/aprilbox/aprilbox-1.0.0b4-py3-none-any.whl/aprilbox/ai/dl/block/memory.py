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

__all__ = ["Memory"]

from copy import deepcopy

import torch
from torch import nn, Tensor
import torch.nn.functional as F


class Memory(nn.Module):
    """ Independent Memory Block
    
    Args:
        in_channel: the channel of input data.
        out_channel: the channel of output data.
        memory_size: the size of the memory block.
    
    References:
        `Unknown`
    """
    
    def __init__(self, in_channel: int,
                 out_channel: int,
                 memory_size: int) -> None:
        super(Memory, self).__init__()
        self.motion_matching_encoder = nn.Sequential(
            nn.Conv3d(in_channel, 64, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(1, 2, 2), stride=(1, 2, 2)),
            nn.Conv3d(64, 128, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2)),
            nn.Conv3d(128, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.Conv3d(256, 256, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.Conv3d(256, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.Conv3d(512, 512, kernel_size=(3, 3, 3), padding=(1, 1, 1)),
            nn.ReLU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2)),
            nn.AdaptiveAvgPool3d([1, None, None]))

        self.motion_context_encoder = deepcopy(self.motion_matching_encoder)

        self.embedder = nn.Sequential(nn.ConvTranspose2d(in_channels=512, out_channels=256, kernel_size=(3, 3),
                                                         stride=(2, 2), padding=(1, 1), output_padding=(1, 1)),
                                      nn.LeakyReLU(0.3, inplace=True),
                                      nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=(3, 3),
                                                         stride=(2, 2), padding=(1, 1), output_padding=(1, 1)),
                                      nn.LeakyReLU(0.3, inplace=True),
                                      nn.ConvTranspose2d(in_channels=128, out_channels=out_channel, kernel_size=(3, 3),
                                                         stride=(2, 2), padding=(1, 1), output_padding=(1, 1)),
                                      nn.LeakyReLU(0.3, inplace=True))

        self.memory_shape = [memory_size, 512]
        self.memory_w = nn.init.normal_(torch.empty(self.memory_shape), mean=0.0, std=1.0)
        self.memory_w = nn.Parameter(self.memory_w, requires_grad=True)

    def forward(self, memory_x: Tensor, phase: bool) -> Tensor:
        memory_x = memory_x.transpose(dim0=1, dim1=2)  # make (N, C, T, H, W) for 3D Conv
    
        motion_encoder = self.motion_context_encoder if phase else self.motion_matching_encoder
        memory_query = torch.squeeze(motion_encoder(memory_x), dim=2)  # make (N, C, H, W)
    
        query_c, query_h, query_w = memory_query.size()[1], memory_query.size()[2], memory_query.size()[3]
        memory_query = memory_query.permute(0, 2, 3, 1)  # make (N, H, W, C)
        memory_query = torch.reshape(memory_query, (-1, query_c))  # make (N * H * W, C)
    
        # memory addressing
        query_norm = F.normalize(memory_query, dim=1)
        memory_norm = F.normalize(self.memory_w, dim=1)
        s = torch.mm(query_norm, memory_norm.transpose(dim0=0, dim1=1))
        addressing_vec = F.softmax(s, dim=1)
        memory_feature = torch.mm(addressing_vec, self.memory_w)
    
        memory_feature = torch.reshape(memory_feature, (-1, query_h, query_w, query_c))  # make (N, H, W, C)
        memory_feature = memory_feature.permute(0, 3, 1, 2)  # make (N, C, H, W) for 2D DeConv
        memory_feature = self.embedder(memory_feature)
    
        return memory_feature
