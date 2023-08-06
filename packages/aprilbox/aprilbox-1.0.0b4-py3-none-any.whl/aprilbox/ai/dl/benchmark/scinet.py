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

__all__ = ["InteractLevel", "SCINet"]

import math

import numpy as np
import torch
from torch import nn, Tensor
import torch.nn.functional as F


class Splitting(nn.Module):
    def __init__(self):
        super(Splitting, self).__init__()

    @classmethod
    def even(cls, x: Tensor) -> Tensor:
        return x[:, ::2, :]

    @classmethod
    def odd(cls, x: Tensor) -> Tensor:
        return x[:, 1::2, :]

    def forward(self, x: Tensor):
        """Returns the odd and even part"""
        return self.even(x), self.odd(x)


class Interaction(nn.Module):
    def __init__(self,
                 in_channel: int,
                 splitting: bool = True,
                 kernel_size: int = 5,
                 dropout: float = 0.5,
                 groups: int = 1,
                 hidden_size: int = 1,
                 INN: bool = True):
        super(Interaction, self).__init__()
        self.modified = INN
        dilation = 1
        if kernel_size % 2 == 0:
            pad_l = dilation * (kernel_size - 2) // 2 + 1  # by default: stride==1
            pad_r = dilation * (kernel_size) // 2 + 1  # by default: stride==1
        else:
            pad_l = dilation * (kernel_size - 1) // 2 + 1  # we fix the kernel size of the second layer as 3.
            pad_r = dilation * (kernel_size - 1) // 2 + 1
        self.splitting = splitting
        self.split = Splitting()

        prev_size = 1
        modules_rho = [
            nn.ReplicationPad1d((pad_l, pad_r)),

            nn.Conv1d(in_channel * prev_size, int(in_channel * hidden_size),
                      kernel_size=kernel_size, dilation=dilation, stride=1, groups=groups),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),

            nn.Dropout(dropout),
            nn.Conv1d(int(in_channel * hidden_size), in_channel,
                      kernel_size=3, stride=1, groups=groups),
            nn.Tanh()
        ]
        modules_eta = [
            nn.ReplicationPad1d((pad_l, pad_r)),
            nn.Conv1d(in_channel * prev_size, int(in_channel * hidden_size),
                      kernel_size=kernel_size, dilation=dilation, stride=1, groups=groups),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            nn.Dropout(dropout),
            nn.Conv1d(int(in_channel * hidden_size), in_channel,
                      kernel_size=3, stride=1, groups=groups),
            nn.Tanh()
        ]

        modules_phi = [
            nn.ReplicationPad1d((pad_l, pad_r)),
            nn.Conv1d(in_channel * prev_size, int(in_channel * hidden_size),
                      kernel_size=kernel_size, dilation=dilation, stride=1, groups=groups),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            nn.Dropout(dropout),
            nn.Conv1d(int(in_channel * hidden_size), in_channel,
                      kernel_size=3, stride=1, groups=groups),
            nn.Tanh()
        ]
        modules_psi = [
            nn.ReplicationPad1d((pad_l, pad_r)),
            nn.Conv1d(in_channel * prev_size, int(in_channel * hidden_size),
                      kernel_size=kernel_size, dilation=dilation, stride=1, groups=groups),
            nn.LeakyReLU(negative_slope=0.01, inplace=True),
            nn.Dropout(dropout),
            nn.Conv1d(int(in_channel * hidden_size), in_channel,
                      kernel_size=3, stride=1, groups=groups),
            nn.Tanh()
        ]
        self.phi = nn.Sequential(*modules_phi)
        self.psi = nn.Sequential(*modules_psi)
        self.rho = nn.Sequential(*modules_rho)
        self.eta = nn.Sequential(*modules_eta)

    def forward(self, x: Tensor):
        if self.splitting:
            (x_even, x_odd) = self.split(x)
        else:
            (x_even, x_odd) = x

        if self.modified:
            x_even = x_even.permute(0, 2, 1)
            x_odd = x_odd.permute(0, 2, 1)

            d = x_odd.mul(torch.exp(self.phi(x_even)))
            c = x_even.mul(torch.exp(self.psi(x_odd)))

            x_even_update = c + self.eta(d)
            x_odd_update = d - self.rho(c)

            return x_even_update, x_odd_update

        else:
            x_even = x_even.permute(0, 2, 1)
            x_odd = x_odd.permute(0, 2, 1)

            d = x_odd - self.rho(x_even)
            c = x_even + self.eta(d)
            return c, d


class InteractLevel(nn.Module):
    def __init__(self,
                 in_channel: int,
                 kernel_size: int,
                 dropout: float,
                 groups: int,
                 hidden_size: int,
                 INN: bool
                 ) -> None:
        super(InteractLevel, self).__init__()
        self.level = Interaction(in_channel=in_channel, splitting=True, kernel_size=kernel_size, dropout=dropout,
                                 groups=groups, hidden_size=hidden_size, INN=INN)

    def forward(self, x: Tensor):
        return self.level(x)


class LevelSCINet(nn.Module):
    def __init__(self,
                 in_channel: int,
                 kernel_size: int,
                 dropout: float,
                 groups: int,
                 hidden_size: int,
                 INN: bool
                 ) -> None:
        super(LevelSCINet, self).__init__()
        self.interact = InteractLevel(in_channel=in_channel, kernel_size=kernel_size, dropout=dropout, groups=groups,
                                      hidden_size=hidden_size, INN=INN)

    def forward(self, x):
        (x_even_update, x_odd_update) = self.interact(x)
        return x_even_update.permute(0, 2, 1), x_odd_update.permute(0, 2, 1)  # even: B, T, D odd: B, T, D


class SCINetTree(nn.Module):
    def __init__(self, in_channel, current_level, kernel_size, dropout, groups, hidden_size, INN):
        super().__init__()
        self.current_level = current_level

        self.work_block = LevelSCINet(
            in_channel=in_channel,
            kernel_size=kernel_size,
            dropout=dropout,
            groups=groups,
            hidden_size=hidden_size,
            INN=INN)

        if current_level != 0:
            self.tree_odd = SCINetTree(in_channel, current_level - 1, kernel_size, dropout, groups, hidden_size, INN)
            self.tree_even = SCINetTree(in_channel, current_level - 1, kernel_size, dropout, groups, hidden_size, INN)

    def zip_up_the_pants(self, even, odd):
        even = even.permute(1, 0, 2)
        odd = odd.permute(1, 0, 2)  # L, B, D
        even_len = even.shape[0]
        odd_len = odd.shape[0]
        mlen = min((odd_len, even_len))
        _ = []
        for i in range(mlen):
            _.append(even[i].unsqueeze(0))
            _.append(odd[i].unsqueeze(0))
        if odd_len < even_len:
            _.append(even[-1].unsqueeze(0))
        return torch.cat(_, 0).permute(1, 0, 2)  # B, L, D

    def forward(self, x):
        x_even_update, x_odd_update = self.work_block(x)
        # We recursively reordered these sub-series. You can run the ./utils/recursive_demo.py to emulate this procedure.
        if self.current_level == 0:
            return self.zip_up_the_pants(x_even_update, x_odd_update)
        else:
            return self.zip_up_the_pants(self.tree_even(x_even_update), self.tree_odd(x_odd_update))


class EncoderTree(nn.Module):
    def __init__(self, in_channel, num_levels, kernel_size, dropout, groups, hidden_size, INN):
        super().__init__()
        self.SCINet_Tree = SCINetTree(
            in_channel=in_channel,
            current_level=num_levels - 1,
            kernel_size=kernel_size,
            dropout=dropout,
            groups=groups,
            hidden_size=hidden_size,
            INN=INN)

    def forward(self, x: Tensor):
        x = self.SCINet_Tree(x)
        return x


class SCINet(nn.Module):
    def __init__(self,
                 input_len: int,
                 output_len: int,
                 input_dim: int = 9,
                 hidden_size: int = 1,
                 num_stacks: int = 1,
                 num_levels: int = 3,
                 num_decoder_layer: int = 1,
                 concat_len: int = 0,
                 groups: int = 1,
                 kernel_size: int = 5,
                 dropout: float = 0.5,
                 single_step_output_One: int = 0,
                 positionalE: bool = False,
                 modified: bool = True,
                 RIN: bool = False):
        super(SCINet, self).__init__()

        self.input_len = input_len
        self.output_len = output_len
        self.num_levels = num_levels

        self.modified = modified


        self.single_step_output_One = single_step_output_One
        self.concat_len = concat_len
        self.pe = positionalE
        self.RIN = RIN
        self.num_decoder_layer = num_decoder_layer

        self.blocks1 = EncoderTree(
            in_channel=input_dim,
            num_levels=num_levels,
            kernel_size=kernel_size,
            dropout=dropout,
            groups=groups,
            hidden_size=hidden_size,
            INN=modified)

        if num_stacks == 2:  # we only implement two stacks at most.
            self.blocks2 = EncoderTree(
                in_channel=input_dim,
                num_levels=num_levels,
                kernel_size=kernel_size,
                dropout=dropout,
                groups=groups,
                hidden_size=hidden_size,
                INN=modified)

        self.stacks = num_stacks

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.bias.data.zero_()

        self.projection1 = nn.Conv1d(self.input_len, self.output_len, kernel_size=1, stride=1, bias=False)
        self.div_projection = nn.ModuleList()
        self.overlap_len = self.input_len // 4
        self.div_len = self.input_len // 6

        if self.num_decoder_layer > 1:
            self.projection1 = nn.Linear(self.input_len, self.output_len)
            for layer_idx in range(self.num_decoder_layer - 1):
                div_projection = nn.ModuleList()
                for i in range(6):
                    lens = min(i * self.div_len + self.overlap_len, self.input_len) - i * self.div_len
                    div_projection.append(nn.Linear(lens, self.div_len))
                self.div_projection.append(div_projection)

        if self.single_step_output_One:  # only output the N_th timestep.
            if self.stacks == 2:
                if self.concat_len:
                    self.projection2 = nn.Conv1d(self.concat_len + self.output_len, 1,
                                                 kernel_size=1, bias=False)
                else:
                    self.projection2 = nn.Conv1d(self.input_len + self.output_len, 1,
                                                 kernel_size=1, bias=False)
        else:  # output the N timesteps.
            if self.stacks == 2:
                if self.concat_len:
                    self.projection2 = nn.Conv1d(self.concat_len + self.output_len, self.output_len,
                                                 kernel_size=1, bias=False)
                else:
                    self.projection2 = nn.Conv1d(self.input_len + self.output_len, self.output_len,
                                                 kernel_size=1, bias=False)

        # For positional encoding
        self.pe_hidden_size = input_dim
        if self.pe_hidden_size % 2 == 1:
            self.pe_hidden_size += 1

        num_timescales = self.pe_hidden_size // 2
        max_timescale = 10000.0
        min_timescale = 1.0

        log_timescale_increment = (
                math.log(float(max_timescale) / float(min_timescale)) /
                max(num_timescales - 1, 1))

        inv_timescales = min_timescale * torch.exp(
            torch.arange(num_timescales, dtype=torch.float32) *
            -log_timescale_increment)
        self.register_buffer('inv_timescales', inv_timescales)

        ### RIN Parameters ###
        if self.RIN:
            self.affine_weight = nn.Parameter(torch.ones(1, 1, input_dim))
            self.affine_bias = nn.Parameter(torch.zeros(1, 1, input_dim))

    def get_position_encoding(self, x):
        max_length = x.size()[1]
        position = torch.arange(max_length, dtype=torch.float32,
                                device=x.device)  # tensor([0., 1., 2., 3., 4.], device='cuda:0')
        temp1 = position.unsqueeze(1)  # 5 1
        temp2 = self.inv_timescales.unsqueeze(0)  # 1 256
        scaled_time = position.unsqueeze(1) * self.inv_timescales.unsqueeze(0)  # 5 256
        signal = torch.cat([torch.sin(scaled_time), torch.cos(scaled_time)], dim=1)  # [T, C]
        signal = F.pad(signal, (0, 0, 0, self.pe_hidden_size % 2))
        signal = signal.view(1, max_length, self.pe_hidden_size)

        return signal

    def forward(self, x):
        assert self.input_len % (np.power(2,
                                          self.num_levels)) == 0  # evenly divided the input length into two parts. (e.g., 32 -> 16 -> 8 -> 4 for 3 levels)
        if self.pe:
            pe = self.get_position_encoding(x)
            if pe.shape[2] > x.shape[2]:
                x += pe[:, :, :-1]
            else:
                x += self.get_position_encoding(x)

        ### activated when RIN flag is set ###
        if self.RIN:
            print('/// RIN ACTIVATED ///\r', end='')
            means = x.mean(1, keepdim=True).detach()
            # mean
            x = x - means
            # var
            stdev = torch.sqrt(torch.var(x, dim=1, keepdim=True, unbiased=False) + 1e-5)
            x /= stdev
            # affine
            # print(x.shape,self.affine_weight.shape,self.affine_bias.shape)
            x = x * self.affine_weight + self.affine_bias

        # the first stack
        res1 = x
        x = self.blocks1(x)
        x += res1
        if self.num_decoder_layer == 1:
            x = self.projection1(x)
        else:
            x = x.permute(0, 2, 1)
            for div_projection in self.div_projection:
                output = torch.zeros(x.shape, dtype=x.dtype).cuda()
                for i, div_layer in enumerate(div_projection):
                    div_x = x[:, :, i * self.div_len:min(i * self.div_len + self.overlap_len, self.input_len)]
                    output[:, :, i * self.div_len:(i + 1) * self.div_len] = div_layer(div_x)
                x = output
            x = self.projection1(x)
            x = x.permute(0, 2, 1)

        if self.stacks == 1:
            ### reverse RIN ###
            if self.RIN:
                x = x - self.affine_bias
                x = x / (self.affine_weight + 1e-10)
                x = x * stdev
                x = x + means

            return x

        elif self.stacks == 2:
            mid_out_put = x
            if self.concat_len:
                x = torch.cat((res1[:, -self.concat_len:, :], x), dim=1)
            else:
                x = torch.cat((res1, x), dim=1)

            # the second stack
            res2 = x
            x = self.blocks2(x)
            x += res2
            x = self.projection2(x)

            ### Reverse RIN ###
            if self.RIN:
                mid_out_put = mid_out_put - self.affine_bias
                mid_out_put = mid_out_put / (self.affine_weight + 1e-10)
                mid_out_put = mid_out_put * stdev
                mid_out_put = mid_out_put + means

            if self.RIN:
                x = x - self.affine_bias
                x = x / (self.affine_weight + 1e-10)
                x = x * stdev
                x = x + means

            return x, mid_out_put
