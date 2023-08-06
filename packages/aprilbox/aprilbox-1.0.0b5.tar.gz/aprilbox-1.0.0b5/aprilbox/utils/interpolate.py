# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/3/2   17:46
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Interpolate"]

import cv2
import numpy as np
from scipy.interpolate import griddata

from ..types import _TNN, ndarray


class Interpolate(object):
    @classmethod
    def _points(cls, points: _TNN) -> _TNN:
        """ Return coordinate matrices from coordinate vectors.

        Args:
            points: The tuple of coordinate vectors, like (array of x, array of y).

        Returns:
            The coordinate matrices.
        """
        x, y = points
        if x.ndim == y.ndim == 1:
            y, x = np.meshgrid(y, x)
        elif x.ndim == y.ndim == 2:
            pass
        elif x.ndim != y.ndim:
            raise ValueError(f"Expected the same dimension, but got x-{x.ndim} and y-{y.ndim}")
        else:
            raise ValueError(f"Expected the dimension less than 2, but got x-{x.ndim} and y-{y.ndim}")
        return x, y
    
    @classmethod
    def point2point(cls, old_points: _TNN, data: ndarray, new_points: _TNN, method="nearest") -> ndarray:
        """Interpolate 1-dimension data(Station/Points Data) in the new coordinate(Station/Points Data).

        Args:
            old_points: The tuple of coordinates whose shape is like (L1), being same with data.
            data: 1-dimension data values, shape like (L1, ).
            new_points: The tuple of new coordinates whose shape is like (m, n).
            method: default: `nearest`. The method of interpolating.

        Returns:

        """
        old_x, old_y = old_points
        assert (old_x.ndim == old_y.ndim == data.ndim == 1), ValueError("Expected 1-dimension of old_points and data!")
        assert (old_x.shape == old_y.shape == data.shape), ValueError("Expected the same shape of old_points and data!")
        new_x, new_y = new_points
        assert (new_x.ndim == new_y.ndim == 1), ValueError("Expected 1-dimension of new_points!")
        return griddata((old_x, old_y), data, (new_x, new_y), method=method)

    @classmethod
    def point2grid(cls, old_points: _TNN, data: ndarray, new_points: _TNN, method="nearest") -> ndarray:
        """Interpolate 1-dimension data(Station/Points Data) in the new coordinate, which is 2-dimension(Grid Data).

        Args:
            old_points: The tuple of coordinates whose shape is like (L1), being same with data.
            data: 1-dimension data values, shape like (L1, ).
            new_points: The tuple of new coordinates whose shape is like (m, n).
            method: default: `nearest`. The method of interpolating.

        Returns:

        """
        old_x, old_y = old_points
        assert (old_x.ndim == old_y.ndim == data.ndim == 1), ValueError("Expected 1-dimension of old_points and data!")
        assert (old_x.shape == old_y.shape == data.shape), ValueError("Expected the same shape of old_points and data!")
        # Check the new coordinate must be 2-dimension
        new_x, new_y = cls._points(new_points)
        assert (new_x.ndim == new_y.ndim == 2), ValueError("Expected 2-dimension of new_points!")
        return griddata((old_x.ravel(), old_y.ravel()), data.ravel(), (new_x, new_y), method=method)
    
    @classmethod
    def grid2point(cls, old_points: _TNN, data: ndarray, new_points: _TNN, method="nearest") -> ndarray:
        """Interpolate 2-dimension data(Grid Data) in the new coordinate(Grid Data).

        Args:
            old_points: The tuple of coordinates whose shape is like (m1, n1), being same with data.
            data: 2-dimension data values, shape like (m1, n1).
            new_points: The tuple of new coordinates whose shape is like (m2, n2).
            method: default: `nearest`. The method of interpolating.

        Returns:

        """
        # Check the old coordinate must be matched with input data.
        old_x, old_y = cls._points(old_points)
        return cls.point2point((old_x.ravel(), old_y.ravel()), data.ravel(), new_points, method=method)

    @classmethod
    def grid2grid(cls, old_points: _TNN, data: ndarray, new_points: _TNN, method="nearest") -> ndarray:
        """Interpolate 2-dimension data(Grid Data) in the new coordinate(Grid Data).

        Args:
            old_points: The tuple of coordinates whose shape is like (m1, n1), being same with data.
            data: 2-dimension data values, shape like (m1, n1).
            new_points: The tuple of new coordinates whose shape is like (m2, n2).
            method: default: `nearest`. The method of interpolating.

        Returns:

        """
        # Check the old coordinate must be matched with input data.
        old_x, old_y = cls._points(old_points)
        return cls.point2grid((old_x.ravel(), old_y.ravel()), data.ravel(), new_points, method=method)
    
    @classmethod
    def downsize_2d(cls, img: ndarray, size: tuple, method: int = cv2.INTER_NEAREST) -> ndarray:
        """ Downsize 2-dimension image within method(default is cv2.INTER_NEAREST)

        Args:
            img: The input 2-dimension image.
            size: The size to reduce.
            method: default: `cv2.INTER_NEAREST`. The method of downsizing.

        Returns:
            The downsized image.
        """
        h, w = img.shape
        _h, _w = size
        scale = min(_h * 1.0 / h, _w * 1.0 / w)
        h = int(h * scale)
        w = int(w * scale)
        img = cv2.resize(img, (w, h), interpolation=method)
        top = (_h - h) // 2
        left = (_w - w) // 2
        bottom = _h - h - top
        right = _w - w - left
        new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,))
        new_img[new_img < 0] = 0
        return new_img
    
    @classmethod
    def downsize_3d(cls, img, size) -> ndarray:
        """ Downsize 3-dimension image.

        Args:
            img: The input 3-dimension image.
            size: The size to reduce.

        Returns:
            The downsized image.
        """
        _, h, w = img.shape
        img = img.transpose([1, 2, 0])
        _w = _h = size
        scale = min(_h * 1.0 / h, _w * 1.0 / w)
        h = int(h * scale)
        w = int(w * scale)
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
        top = (_h - h) // 2
        left = (_w - w) // 2
        bottom = _h - h - top
        right = _w - w - left
        new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        new_img = new_img.transpose([2, 0, 1])
        return new_img
