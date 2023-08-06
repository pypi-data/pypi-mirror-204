# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   14:24
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["_NUMBER", "_NNUMBER",
           "_TNN", "_TII",

           "ndarray", "Optional", "Union", "Tuple",
           "ContingencyTable", "Property"]

from collections import namedtuple
from typing import Optional, Union, Tuple

from numpy import ndarray


_NNUMBER = Union[None, ndarray, float, int]
_NUMBER = Union[ndarray, float, int]

_TNN = Tuple[ndarray, ndarray]
_TII = Tuple[int, int]



ContingencyTable = namedtuple("ContingencyTable", ["tp", "fp", "fn", "tn"], defaults=(None, None, None, None))
"""ContingencyTable. Including obj:`tp` 、:obj:`fp` 、:obj:`fn` 和 :obj:`tn` 。

   ============================  =============  =============
    Observation  \\  Forecast        Positive      Negative
   ============================  =============  =============
               Positive               tp              fn
               Negative               fp              tn
   ============================  =============  =============

"""
ContingencyTable.tp.__doc__ = "int: Number of hit. There is no matching classification while it is -1. Default: ``None``."
ContingencyTable.fp.__doc__ = "int: Number of missing. There is no matching classification while it is -1. Default: ``None``."
ContingencyTable.fn.__doc__ = "int: Number of far alarm. There is no matching classification while it is -1. Default: ``None``."
ContingencyTable.tn.__doc__ = "int: Number of negative correct. There is no matching classification while it is -1. Default: ``None``."


Property = namedtuple("Property", ["data", "label", "all_prop", "props"], defaults=(None, None, None, None))
"""Property of 2-dimension data."""
Property.data.__doc__ = "np.ndarray:  2-dimension data value. Default: ``None``."
Property.label.__doc__ = "np.ndarray: Label connected regions of an integer array from `skimage.measure.label`.  Default: ``None``."
Property.all_prop.__doc__ = ":obj:`skimage.measure._regionprops.RegionProperties`: Measure properties of labeled image regions from `skimage.measure.regionprops`. Default: ``None``."
Property.props.__doc__ = "list : Properites from `skimage.measure.regionprops`. Default: ``None``."

