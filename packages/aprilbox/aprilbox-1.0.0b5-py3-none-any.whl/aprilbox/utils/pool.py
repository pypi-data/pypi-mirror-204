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

__all__ = ["sub_matrices", "pool2d"]

import numpy as np

from ..types import Optional, ndarray, _TII


def sub_matrices(x: ndarray, window_size: tuple, stride: tuple) -> ndarray:
    """
    Get a strided sub-matrices view of an ndarray.
    
    Args:
    
    
    See Also:
        skimage.util.shape.view_as_windows()
    """
    m, n = x.shape
    sm_x, sn_x = x.strides
    km, kn = window_size
    sm, sn = stride
    # view_shape = (1 + (m - km) // sm, 1 + (n - kn) // sn, km, kn) + x.shape[2:]
    view_shape = (1 + (m - km) // sm, 1 + (n - kn) // sn, km, kn)
    # strides = (sm * sm_x, sn * sn_x, sm_x, sn_x) + x.strides[2:]
    strides = (sm * sm_x, sn * sn_x, sm_x, sn_x)
    return np.lib.stride_tricks.as_strided(x, view_shape, strides=strides)


def pool2d(data: ndarray,
           window_size: _TII,
           stride: Optional[_TII] = None,
           method: str = "max",
           pad: bool = False) -> ndarray:
    """Overlapping pooling on 2D or 3D data.
    
    
    Args:
        data: The input data, shape  is like m * n.
        window_size: The window size for pooling, shape is like km * kn.
        stride: Default ``None``. The stride of pooling. It is same with the window size while it  is None.
        method: Default ``max``. The method of pooling, optional ``max`` or ``mean.
        pad: Default ``False``. Choose whether to pad the data, or not. If True, the shape of output is like m/s * n/s.
             If False, the shape of output is like (m-km)//s+1 * (n-kn)//s+1. The s is the length of stride.

    Returns:
         The pooling data.
    """
    assert data.ndim == 2, NotImplementedError(f"Only support 2D data! The dimensionality of the data is: {data.ndim}!")
    m, n = data.shape
    km, kn = window_size
    
    if stride is None:
        stride = (km, kn)
    sm, sn = stride
    
    if method not in ["mean", "max"]:
        raise NotImplementedError(f"Only support pooling method is \"mean\" and \"max\", but got {method}!")
    
    def self_ceil(x, kx):
        return int(np.ceil(x / float(kx)))
    
    if pad:
        size = ((self_ceil(m, sm) - 1) * sm + km, (self_ceil(n, sn) - 1) * sn + kn) + data.shape[2:]
        data_pad = np.full(size, np.nan)
        data_pad[km // 2:m + km // 2, kn // 2:n + kn // 2, ...] = data
    else:
        data_pad = data[:(m - km) // sm * sm + km, :(n - kn) // sn * sn + kn, ...]
    
    view = sub_matrices(data_pad, window_size, stride)
    
    if method == "max":
        return np.nanmax(view, axis=(2, 3))
    else:
        return np.nanmean(view, axis=(2, 3))
