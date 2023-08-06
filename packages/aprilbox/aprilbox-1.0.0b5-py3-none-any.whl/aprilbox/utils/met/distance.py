# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:34
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Distance"]

import numpy as np

from ...data import ER
from ...types import _NUMBER


class Distance(object):
    @classmethod
    def euclidean(cls, x1: _NUMBER, y1: _NUMBER, x2: _NUMBER, y2: _NUMBER) -> _NUMBER:
        """Calculate Euclidean distance.

        :math:`Distance = \\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}`

        Args:
            x1 : x of start point
            y1 : y of start point
            x2 : x of end point
            y2 : y of end point

        Returns:
            Euclidean distance
        """
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @classmethod
    def haversine(cls, lon1: _NUMBER, lat1: _NUMBER, lon2: _NUMBER, lat2: _NUMBER) -> _NUMBER:
        """Calculate Haversine distance.

        :math:`Distance = 2 * r * \\arcsin{\\sqrt{\\sin^2{(\\frac{\\phi_2 - \\phi_1}{2})} + \\cos{\\phi_1} * \\cos{\\phi_2} * \\sin^2{(\\frac{\\lambda_2 - \\lambda_1}{2})}}}`

        Args:
            lon1: Longitude of point 1.
            lat1: Latitude of point 1.
            lon2: Longitude of point 2.
            lat2: Latitude of point 2.

        Returns:
            Haversine distance, Unit: km.
        """
        # degree to radians
        lon1, lon2 = np.deg2rad(lon1), np.deg2rad(lon2)
        lat1, lat2 = np.deg2rad(lat1), np.deg2rad(lat2)
        # calculate distance
        part1 = np.sin((lat2 - lat1) / 2) ** 2
        part2 = np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
        return 2.0 * ER * np.arcsin((part1 + part2) ** 0.5)

    @classmethod
    def vincenty(cls, lon1: _NUMBER, lat1: _NUMBER, lon2: _NUMBER, lat2: _NUMBER,
                 item: int) -> _NUMBER:
        """Calculate Vincenty distance.

        :math: `Distance = `

        Args:
            lon1:
            lat1:
            lon2:
            lat2:
            item: Default `20`. The number of limit iter.

        Returns:
            Vincenty distance.
        """
        # todo
        # f = 1 / 298.257223563   # 地球椭圆 WGS84 椭圆扁率
        # L = (lon2 - lon1) * np.pi / 180
        # u1 = np.arctan((1 - f) * np.tan(lat1 * np.pi / 180))
        # u2 = np.arctan((1 - f) * np.tan(lat2 * np.pi / 180))
        # sin_u1, cos_u1 = np.sin(u1), np.cos(u1)
        # sin_u2, cos_u2 = np.sin(u2), np.cos(u2)
        #
        # step, step_p = L, 2 * np.pi
        # item = 20
        # while abs(step - step_p) > 1e-12 and item > 0:
        #     sinLambda, cosLambda = np.sin(step), np.cos(step)
        #     sinSigma = np.sqrt((cos_u2 * sinLambda) ** 2 + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cosLambda) ** 2)
        #     cosSigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cosLambda
        #     sigma = np.arctan2(sinSigma, cosSigma)
        #     sinAlpha = cos_u1 * cos_u2 * sinLambda / sinSigma
        #     cosSqAlpha = 1 - sinAlpha ** 2
        #     if cosSqAlpha == 0:
        #         cos2SigmaM = 0
        #     else:
        #         cos2SigmaM = cosSigma - 2 * sin_u1 * sin_u2 / cosSqAlpha
        #     C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        #     step_p, step = step, L + (1 - C) * f * sinAlpha * (
        #                 sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))
        #     item -= 1
        # if item == 0:
        #     raise ValueError("Vincenty 公式未收敛")
        # uSq = cosSqAlpha * (cls.ERA ** 2 - cls.ERB ** 2) / (cls.ERB ** 2)
        # A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
        # B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
        # delta_sigma = B * sinSigma * (cos2SigmaM + B / 4 * ())
        # return cls.ERB * A * (sigma - delta_sigma)
        raise NotImplementedError("Not Implemented yet!")

