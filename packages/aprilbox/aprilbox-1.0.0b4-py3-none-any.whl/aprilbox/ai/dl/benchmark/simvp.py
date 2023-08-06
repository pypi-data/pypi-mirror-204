# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/7   16:16
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["SimVP"]

from typing import Optional

from torch import nn


class SimVP(nn.Module):
    """SimVP Model
        Implementation of `SimVP: Simpler yet Better Video Prediction
        <https://arxiv.org/abs/2206.05099>`_.
    """
    def __init__(self, shape: tuple = (12, 4, 64, 64),
                 hid_S: int = 16,
                 hid_T: int = 256,
                 N_S: int = 4,
                 N_T: int = 8,
                 incep_ker: Optional[list] = None,
                 groups: int = 8,
                 **kwargs) -> None:
        super(SimVP, self).__init__()
#         t, c, h, w = shape
#         if incep_ker is None:
#             incep_ker = [3, 5, 7, 11]
#
#         self.enc = Encoder(c, hid_S, N_S)
#         self.dec = Decoder(hid_S, c, N_S)
#         self.hid = Mid_Xnet(t*hid_S, hid_T, N_T, incep_ker, groups)
#
#
#     def forward(self, x_raw):
#         b, t, c, h, w = x_raw.shape
#         x = x_raw.view(b*t, c, h, w)
#
#         embed, skip = self.enc(x)
#         _, _c, _h, _w = embed.shape
#
#         z = embed.view(b, t, _c, _h, _w)
#         hid = self.hid(z)
#         hid = hid.reshape(b*t, _c, _h, _w)
#
#         y = self.dec(hid, skip)
#         y = y.reshape(b, t, c, h, w)
#         return y
