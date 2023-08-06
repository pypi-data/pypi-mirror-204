"""
Function

- spatial-channel

PSA -> Mine features in spatial and channel
----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:32
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""
__all__ = ["PSA"]

import torch
import torch.nn as nn


def constant_init(module,
                  val,
                  bias=0) -> None:
    if hasattr(module, 'weight') and module.weight is not None:
        nn.init.constant_(module.weight, val)
    if hasattr(module, 'bias') and module.bias is not None:
        nn.init.constant_(module.bias, bias)


def kaiming_init(module,
                 a=0,
                 mode="fan_out",
                 nonlinearity="relu",
                 bias=0,
                 distribution="normal") -> None:
    assert distribution in ["uniform", "normal"]
    if distribution == "uniform":
        nn.init.kaiming_uniform_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
    else:
        nn.init.kaiming_normal_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
    if hasattr(module, "bias") and module.bias is not None:
        nn.init.constant_(module.bias, bias)


class PSA(nn.Module):
    """Polarized Self-Attention
    Polarized Self-Attention with two layout --parallel and sequential.
    
    Args:
        in_channel : The channel number of the input data.
        out_channel : default: same with `in_channel`. The channel number of the output data.
        layout : default: `parallel`. Only accept `parallel` or `sequential`. Decide the layout of the self-attention.
    
    References:
        `[1] Liu H, Liu F, Fan X, et al. Polarized Self-Attention: Towards High-quality Pixel-wise Regression[J]. 2021.`__
        .. __: https://github.com/DeLightCMU/PSA
    """
    def __init__(self, in_channel: int,
                 out_channel: int = None,
                 layout: str = "parallel") -> None:
        super(PSA, self).__init__()
        if out_channel is None:
            out_channel = in_channel
        self.inner_channel = out_channel // 2
        self.out_channel = out_channel
        
        self.spatial_q = nn.Conv2d(in_channel, self.inner_channel, (1, 1), stride=(1, 1), padding=(0, 0), bias=False)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.spatial_soft = nn.Softmax(dim=2)
        self.spatial_v = nn.Conv2d(in_channel, self.inner_channel, (1, 1), stride=(1, 1), padding=(0, 0), bias=False)
        
        self.channel_q = nn.Conv2d(in_channel, 1, (1, 1), stride=(1, 1), padding=(0, 0), bias=False)
        self.channel_soft = nn.Softmax(dim=2)
        self.channel_v = nn.Conv2d(in_channel, self.inner_channel, (1, 1), stride=(1, 1), padding=(0, 0), bias=False)
        self.channel_z = nn.Conv2d(self.inner_channel, out_channel, (1, 1), stride=(1, 1), padding=(0, 0), bias=False)
        self.ln = nn.LayerNorm(out_channel)
        self.sigmoid = nn.Sigmoid()
        
        self.reset_parameters()
        self.layout = layout.lower()

    def reset_parameters(self) -> None:
        kaiming_init(self.spatial_q, mode='fan_in')
        kaiming_init(self.spatial_v, mode='fan_in')
        kaiming_init(self.channel_q, mode='fan_in')
        kaiming_init(self.channel_v, mode='fan_in')
    
        self.spatial_q.inited = True
        self.spatial_v.inited = True
        self.channel_q.inited = True
        self.channel_v.inited = True

    def channel_pool(self, x: torch.Tensor) -> torch.Tensor:
        """Channel-only Self-Attention

        Args:
            x: input data.

        Returns:
            channel-only branch
        """
        batch, channel, height, width = x.size()
    
        # ------------------------ Wq ---------------------------------------
        # [N, 1, H, W]  -- conv(1 * 1)
        context_mask = self.channel_q(x)
        # [N, H*W, 1]   -- Reshape
        context_mask = context_mask.view(batch, 1, height * width)
        # [N, H*W, 1]   -- Softmax
        context_mask = self.channel_soft(context_mask)
    
        # ------------------------ Wv ---------------------------------------
        # [N, C//2, H, W]  -- conv(1 * 1)
        input_x = self.channel_v(x)
        # [N, C//2, H*W]   -- Reshape
        input_x = input_x.view(batch, self.inner_channel, height * width)
    
        # -------------------------------------------------------------------
        # [N, C//2, 1]      -- Matmul
        context = torch.matmul(input_x, context_mask.transpose(1, 2))
        # [N, C, 1, 1]      -- conv(1 * 1) + LayerNorm
        context = self.ln(self.channel_z(context.unsqueeze(-1)).view(batch, self.out_channel))
        # [N, C, 1, 1]      -- Sigmoid
        mask_ch = self.sigmoid(context.view(batch, self.out_channel, 1, 1))
    
        # [N, C, H, W]      -- *
        out = x * mask_ch
        return out

    def spatial_pool(self, x: torch.Tensor) -> torch.Tensor:
        """Spatial-only Self-Attention

        Args:
            x : input data.

        Returns:
            spatial-only branch
        """
        batch, channel, height, width = x.size()
    
        # ------------------------ Wq ---------------------------------------
        # [N, C//2, H, W]  -- conv(1 * 1)
        g_x = self.spatial_q(x)
        # [N, C//2, 1, 1]  -- Global Pooling
        avg_x = self.avg_pool(g_x)
        # [N, 1, C//2]     -- Reshape
        avg_x = avg_x.view(batch, self.inner_channel, 1).permute(0, 2, 1)
        # [N, 1, C//2]     -- Softmax
        avg_x = self.spatial_soft(avg_x)
    
        # ------------------------ Wv ---------------------------------------
        # [N, C//2, H, W]     -- conv(1 * 1)
        theta_x = self.spatial_v(x)
        # [N, C//2, H*W]      -- reshape
        theta_x = theta_x.view(batch, self.inner_channel, height * width)
    
        # -------------------------------------------------------------------
        # [N, 1, H*W]      -- Matmul
        context = torch.matmul(avg_x, theta_x)
        # [N, 1, H, W]      -- Reshape
        context = context.view(batch, 1, height, width)
        # [N, 1, H, W]      -- Sigmoid
        mask_sp = self.sigmoid(context)
        # [N, C, H, W]      -- *
        out = x * mask_sp
        return out
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.layout == "parallel":
            # Channel-only Self-Attention
            channel_out = self.channel_pool(x)
            # Spatial-only Self-Attention
            spatial_out = self.spatial_pool(x)
            return channel_out + spatial_out
        elif self.layout == "sequential":
            # Channel-only Self-Attention
            channel_out = self.channel_pool(x)
            # Spatial-only Self-Attention
            spatial_out = self.spatial_pool(channel_out)
            return spatial_out
        else:
            raise ValueError("Input of \"method\" isn't in either \"parallel\" and \"sequential\", please check input!")
