# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/27   16:38
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Precipitation"]

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

from .base import Base
from ..types import *


class Precipitation(Base):
    @classmethod
    def contourf(cls, data:_NNUMBER, lat:_NNUMBER = None, lon:_NNUMBER = None, **kwargs) -> None:
        """ Contourf for precipitation.

        Args:
            data: Precipitation
            lat: Coordination of latitude
            lon: Coordination of longitude
            **kwargs:

        """
        figsize = kwargs.pop("figsize", (10, 10))
        save_path = kwargs.pop("save_path", "./precipitation.png")
        threshold = kwargs.pop("threshold", [0, 0.1, 2, 4, 6, 8, 10, 20, 25, 50, 999])
        dpi = kwargs.pop("dpi", 400)


        kwargs.update(dict(cmap=cls.PRE1H.CMAP, norm=BoundaryNorm(threshold, cls.PRE1H.CMAP.N)))


        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        if (lat is None) or (lon is None):
            img = ax.contourf(data, levels=threshold, **kwargs)
        else:
            img = ax.contourf(lon, lat, data, levels=threshold, **kwargs)
        plt.colorbar(img)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()


