# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:41
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Extend", "DataReader"]


from pathlib import Path
from typing import Optional, Union

from netCDF4 import Dataset
import numpy as np
import pandas as pd
import pygrib

from .constant import GRIB2DICT
from ...types import _NUMBER


class Extend(object):
    """ The extend information of location.

    Includes `slon`, `elon`, `slat`, elat`, `error` and `plev`.

    Attributes:
        slat(float): start latitude.
        elat(float): end latitude.
        slon(float): start longitude.
        elon(float): end longitude.
        error(float): Default ``0.05``.The error of the coordination.
        plev(list): Default ``None``.The height of pressure height.

    Args:
        slat: start latitude.
        elat: end latitude.
        slon: start longitude.
        elon: end longitude.
        error: Default ``0.05``.The error of the coordination.
        plev: Default ``None``.The height of pressure height.
    """

    def __init__(self, slat: _NUMBER, elat: _NUMBER, slon: _NUMBER, elon: _NUMBER, error: float = 0.05,
                 plev: Union[list, float, int, None] = None):
        self._slat = slat
        self._elat = elat
        self._slon = slon
        self._elon = elon
        self._error = error
        self._plev = plev

    @property
    def slat(self) -> float:
        return self._slat - self._error

    @property
    def elat(self) -> float:
        return self._elat + self._error

    @property
    def slon(self) -> float:
        return self._slon - self._error

    @property
    def elon(self) -> float:
        return self._elon + self._error

    @property
    def error(self) -> float:
        return self._error

    @property
    def plev(self) -> Optional[list]:
        if self._plev is None:
            return None
        elif isinstance(self._plev, list):
            return self._plev
        elif isinstance(self._plev, (float, int)):
            return [self._plev]
        else:
            raise ValueError(f'>>>Expected "plev" is the U_FIN or list, but got {self._plev}!')


class DataReader(object):
    """ Reader of grid data.

    Read the data from key words like :obj:`path`, :obj:`vnames`, :obj:`extent` and so on.
    """
    GRIBDICT = GRIB2DICT

    @classmethod
    def load(cls, path: str or Path, vnames: list, extend: dict, acc: int = 2, gribdict: Optional[dict] = None,
             name_lat: str = "Lat", name_lon: str = "Lon", surface: bool = True, name_height: str = "Plev") -> dict:
        """ Load grid data.

        Read data within key words including path, vnames, locational extend, accuracy, and so on.

        Args:
            path : The path of the data.
            vnames : The names of variables.
            extend: The extend of location. Key of the dict includes `slon`, `elon`, `slat`, elat` and `error`.
            acc: Default ``2``. The fractional precision of the read data retention.
            gribdict: Default ``None``. The dictionary of grib2 for selecting variables.
            name_lat: Default ``Lat``. The name of the coordination - latitude.
            name_lon: Default ``Lon``. The name of the coordination - longitude.
            surface: Default ``True``. Raed surface data or upar data.
            name_height: Default ``Plev``. The name of the coordination - pressure height. Valid only when :obj:`surface`= `True`.

        Returns:
            The container of the grid data

        Examples:

            >>> path1, path2 = "./././path1", "./././path2"
            >>> pre_dict = dict(PRE_1h=dict(parameterName="Total precipitation"))
            >>> cmpas = DataReader.load(path=path1, vnames=["PRE_1h"], gribdict=pre_dict)    # 读取CMPAS实况数据
            >>> qpf = DataReader.load(path=path2, vnames=["PRE_1h"], acc=2)                  # 读取QPF-DL预报产品数据
        """
        # 若数据路径不存在，则返回空容器
        p = Path(path)
        if not p.exists():
            return dict()

        error = pow(10, -1 * acc) / 2
        assert isinstance(extend, dict), ValueError("请输入经纬度落区！")
        extend = Extend(error=error, **extend)

        # 若基类GRIB2字典表不包含提取变量的关键信息，则传入更新
        if isinstance(gribdict, dict):
            for key, value in gribdict.items():
                setattr(cls.GRIBDICT, key, value)

        # 选择格点数据读取方式
        ext = p.suffix.lower()
        if ext == ".nc":
            return cls.load_nc(path, vnames, extend=extend, name_lat=name_lat, name_lon=name_lon, surface=surface,
                               name_height=name_height)
        elif ext in [".grb2", ".bin"]:
            return cls.load_grb(path, vnames, extend=extend, name_lat=name_lat, name_lon=name_lon, surface=surface)
        else:
            return dict()

    @classmethod
    def load_nc(cls, path: str or Path, vnames: list, extend: Extend,
                name_lon: str = "Lon", name_lat: str = "Lat",
                surface: bool = True, name_height: str = "Plev") -> dict:
        """Load grid data in NetCDF format.

        Args:
            path : The path of the data.
            vnames : The names of variables.
            extend: The extend of location. Key of the dict includes `slon`, `elon`, `slat`, elat` and `error`.
            name_lat: Default ``Lat``. The name of the coordination - latitude.
            name_lon: Default ``Lon``. The name of the coordination - longitude.
            surface: Default ``True``. Raed surface data or upar data.
            name_height: Default ``Plev``. The name of the coordination - pressure height. Valid only when :obj:`surface`= `True`.

        Returns:
            The container of the grid data from NetCDF format data.
        """
        data = Dataset(path)
        # todo 多维NC数据的读取
        x_coord = data.variables[name_lon][:]
        y_coord = data.variables[name_lat][:]
        nx = np.where((extend.slon <= x_coord) & (x_coord <= extend.elon))[0]
        ny = np.where((extend.slat <= y_coord) & (y_coord <= extend.elat))[0]
        # 当为高空格点数据时的前处理
        if not surface:
            z_coord = data.variables[name_height]
            nz = np.where(np.isin(z_coord, extend.plev))
        else:
            nz = None
        # 存放坐标轴
        cntr = {name_lon: x_coord[nx], name_lat: y_coord[ny]}
        for vname in vnames:
            if vname in data.variables.KEYS():
                if surface:
                    cntr[vname] = data.variables[vname][ny, nx]
                else:
                    cntr[vname] = data.variables[vname][nz, ny, nx]
        return cntr

    @classmethod
    def load_grb(cls, path: str or Path, vnames: list, extend: Extend,
                 name_lat: str = "Lat", name_lon: str = "Lon",
                 surface: bool = True, ) -> dict:
        """Load grid data in GRIB2 format.

        Args:
            path : The path of the data.
            vnames : The names of variables.
            extend: The extend of location. Key of the dict includes `slon`, `elon`, `slat`, elat` and `error`.
            name_lat: Default ``Lat``. The name of the coordination - latitude.
            name_lon: Default ``Lon``. The name of the coordination - longitude.
            surface: Default ``True``. Raed surface data or upar data.

        Returns:
            The container of the grid data from GRIB2 format data.
        """

        if not surface:
            # todo GRIB2 格式数据暂不支持3-D 格点读取
            raise NotImplementedError(f"Loading upar GRIB2 data have not implemented yet!")
        cntr = dict()
        with pygrib.open(str(path)) as messages:
            for vname in vnames:
                message = messages.select(**getattr(cls.GRIBDICT, vname))
                if len(message) == 1:
                    message = message[0]
                elif len(message) > 1:
                    message = message[0]
                    Warning(f">>> GRIB DATA have more than one message of {vname}!!!")
                else:
                    Warning(f">>> GRIB DATA have no one message of {vname}!!!")
                    continue
                data, lat, lon = message.data(lat1=extend.slat, lon1=extend.slon,
                                              lat2=extend.elat, lon2=extend.elon)
                cntr[vname] = data
                # 当不从数据中读取坐标信息且数据容器中不包含坐标信息时，存放坐标信息
                if (name_lon not in vnames) and (name_lon not in cntr):
                    cntr[name_lon] = lon
                if (name_lat not in vnames) and (name_lat not in cntr):
                    cntr[name_lat] = lat
        return cntr

    @classmethod
    def read_boundary(cls, path: Union[str, Path, list], vname: str = "qxCode",
                      name_lat: str = "lat", name_lon: str = "lon") -> dict:
        """ Read the boundary information of administration

        Args:
            path: The list of the paths which include grid administration and csv administration.
            vname : The vname of variable.
            name_lat: Default ``Lat``. The name of the coordination - latitude.
            name_lon: Default ``Lon``. The name of the coordination - longitude.

        Returns:

        """

        def read_nc(p: Path) -> dict:
            tmp = Dataset(p)
            b_code = tmp.variables[vname][:]
            b_lat = tmp.variables[name_lat][:]
            b_lon = tmp.variables[name_lon][:]
            return dict(BORDERCODE=b_code, BORDERLAT=b_lat, BORDERLON=b_lon)

        def read_cvs(p: Path) -> dict:
            return dict(BORDERLIST=pd.read_csv(p, low_memory=False))

        if isinstance(path, list):
            path = [Path(tmp_path) for tmp_path in path]
        elif isinstance(path, str):
            path = [Path(path)]
        elif isinstance(path, Path):
            path = [path]
        else:
            raise ValueError("Path is Error!")

        boundary = dict()
        for tmp_path in path:
            if tmp_path.suffix == ".nc":
                boundary.update(read_nc(tmp_path))
            elif tmp_path.suffix == ".txt":
                boundary.update(read_cvs(tmp_path))
            else:
                raise ValueError("Path is Error!")
        return boundary