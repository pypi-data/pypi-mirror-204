# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   15:35
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["Factors"]

import numpy as np

from ...data import KELVIN
from ...types import Tuple, _NUMBER


class Factors(object):
    @classmethod
    def saturation_vapor_pressure(cls, temperature: _NUMBER) -> _NUMBER:
        """Calculate the saturation water vapor (partial) pressure.

        :math: e(TMP) = 6.112 e^\frac{17.67T}{T + 243.5}

        Args:
            temperature: Air temperature

        Returns:
            saturation vapor pressure
        """
        # Converted from original in terms of C to use kelvin. Using raw absolute values of C in
        # a formula plays havoc with units support.
        return 6.112 * np.exp(17.67 * (temperature - KELVIN) / (temperature - KELVIN + 243.5))

    @classmethod
    def rhu_from_dpt(cls, tmp: _NUMBER, dpt: _NUMBER) -> _NUMBER:
        """Calculate the relative humidity.

        Uses temperature and dewpoint to calculate relative humidity as the ratio of vapor
        pressure to saturation vapor pressures.

        :math: `RHU = \frac{e(T_temperature)}{e(T_dewpoint)}`

        Args:
            tmp: Air temperature, Unit: deg.
            dpt: Dew point temperature, Unit: deg.

        Returns:
            relative humidity, Unit: 1.
        """
        assert isinstance(tmp, (np.ndarray, float, int)), ValueError(f"Expect get the number of the temperature,"
                                                                     f" but got {type(tmp)}")
        assert isinstance(dpt, (np.ndarray, float, int)), ValueError(
            f"Expect get the number of the dew point temperature,"
            f" but got {type(dpt)}")
        return cls.saturation_vapor_pressure(dpt) / cls.saturation_vapor_pressure(tmp)

    @classmethod
    def wind_decompose(cls, speed: _NUMBER, direction: _NUMBER) -> Tuple[np.ndarray, np.ndarray]:
        """ Decompose wind vector, including wind speed and wind direction, into u-wind and v-wind.

        Args:
            speed: Wind speed, Unit: m/s.
            direction: Wind direction, Unit: deg.

        Returns:
            u-wind(Unit: m/s) and v-wind(Unit: m/s)
        """
        assert isinstance(speed, (np.ndarray, float, int)), ValueError(f"Expect get the number of the wind speed,"
                                                                       f" but got {type(speed)}")
        assert isinstance(direction, (np.ndarray, float, int)), ValueError(
            f"Expect get the number of the wind direction,"
            f" but got {type(direction)}")

        u = speed * np.cos(direction * np.pi / 360)
        v = speed * np.sin(direction * np.pi / 360)
        return u, v

    @classmethod
    def wind_compose(cls, u: _NUMBER, v: _NUMBER) -> Tuple[np.ndarray, np.ndarray]:
        """ Compose u-wind and v-wind into wind vector which includes wind speed and wind direction.

        Args:
            u : u-wind, Unit: m/s
            v : v-wind, Unit: m/s

        Returns:
            wind speed(Unit: m/s) and wind direction(Unit: deg)
        """
        assert isinstance(u, (np.ndarray, float, int)), ValueError(f"Expect get the number of the u-wind,"
                                                                   f" but got {type(u)}")
        assert isinstance(v, (np.ndarray, float, int)), ValueError(f"Expect get the number of the v-wind,"
                                                                   f" but got {type(v)}")

        ws = np.sqrt(np.square(u) + np.square(v))
        wd = 270.0 - np.arctan2(v, u) * 180.0 / np.pi
        wd = wd % 360.0
        return ws, wd