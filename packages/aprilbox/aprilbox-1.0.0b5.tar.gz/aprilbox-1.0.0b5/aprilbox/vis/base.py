# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/27   16:39
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Base"]

import numpy as np
from matplotlib.colors import ListedColormap


class PRE1H(object):

    HEX = ["none", "#A7EF8C", "#3DA607", "#5CB9FD", "#0001FA", "#03724D", "#F905F1", "#E84A00", "#9F3815", "#500200"]
    CMAP = ListedColormap(HEX)


class Base(object):
    PRE1H = PRE1H()
