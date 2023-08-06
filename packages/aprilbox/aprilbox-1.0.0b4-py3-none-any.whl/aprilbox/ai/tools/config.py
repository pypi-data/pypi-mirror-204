# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:26
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["NetConfig"]

from typing import Union, List, Tuple


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class NetConfig(object):
    """The basic configuration for the neural network.

    Args:
        batch: The batch size of the input data.
        devices_ids: The ids of the GPU devices.
        shape: The shape of the input data.
        data_max: The maximum of the input data.
    """

    def __init__(self, batch: int = 4,
                 devices_ids: Union[None, int, list] = None,
                 shape: Tuple[int, int] = (64, 64),
                 data_max: Union[int, float] = 300,
                 lr: float = 1e-3,
                 **kwargs) -> None:
        self._batch = batch
        self._pre_devices(devices_ids)
        self._shape = shape
        self._data_max = data_max
        self._lr = lr
        for name, val in kwargs.items():
            if name.lower() in ["batchsize", "devices"]:
                raise ValueError(f"Unexpected input of the \"kwargs\": {name}, it is repeated input, please check it!")
            else:
                setattr(self, name, val)

    def _pre_devices(self, devices_ids: Union[None, int, list]) -> None:
        if devices_ids is None:
            self._devices_ids = [0]
        elif isinstance(devices_ids, list):
            self._devices_ids = devices_ids
        elif isinstance(devices_ids, int):
            self._devices_ids = [devices_ids]
        else:
            raise TypeError(f"Expected got int or list of the \"devices\", but got {devices_ids}, please check it!")

    @property
    def BATCHSIZE(self) -> int:
        """The batch size of the input data."""
        return self._batch

    @property
    def DATAMAX(self) -> Union[int, float]:
        """The maximum of the input data."""
        return self._data_max

    @property
    def DEVICES_IDS(self) -> List[int]:
        """The ids of the GPU devices."""
        return self._devices_ids

    @property
    def DEVICES(self) -> List[str]:
        """The list of GPU devices."""
        return [f"cuda: {idx}" for idx in self._devices_ids]

    @property
    def LR(self) -> float:
        """The learning rate of the neural network"""
        return self._lr

    @property
    def SHAPE(self) -> tuple:
        """The shape of the input data."""
        return self._shape