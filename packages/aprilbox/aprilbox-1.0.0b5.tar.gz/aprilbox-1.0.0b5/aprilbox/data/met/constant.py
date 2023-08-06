# coding: utf-8
"""
Function

----------------------------------
Version    : 0.0.1
Date       : 2023/4/19   17:19
----------------------------------
Author     : April
Contact    : fanglwh@outlook.com
"""

__all__ = ["KELVIN",
           "ER", "ERA", "ERB",
           "Threshold", "GRIB2DICT"]

KELVIN = 273.15         # Kelvin zero temperature, Unit: K
ER = 6371.0088          # Radius of Earth, Unit: km
ERA = 6378.137          # Radius of Earth, Unit: km
ERB = 6356.752314245    # Radius of Earth, Unit: km

class Threshold(object):
    """常用阈值表
    """

    @property
    def cref(self) -> list:
        """雷达回波反射率阈值: [-5, 0, 15, 35, 100]"""
        return [-5, 0, 15, 35, 100]

    @property
    def pvalue(self) -> list:
        """概率预报阈值: [0, 50, 101]"""
        return [0, 50, 101]

    @property
    def rain_1h(self) -> list:
        """1小时累积降雨阈值: [-5, 0, 15, 35, 100]"""
        return [0, 0.1, 2.5, 8.0, 16.0, 150]

    @property
    def rain_3h(self) -> list:
        """3小时累积降雨阈值: [0, 0.1, 3, 10, 20, 50, 70, 300]"""
        return [0, 0.1, 3, 10, 20, 50, 70, 300]

    @property
    def rain_6h(self) -> list:
        """6小时累积降雨阈值: [0, 0.1, 4, 13, 25, 60, 120, 999]"""
        return [0, 0.1, 4, 13, 25, 60, 120, 999]

    @property
    def rain_12h(self) -> list:
        """12小时累积降雨阈值: [0, 0.1, 5, 15, 30, 70, 140, 999]"""
        return [0, 0.1, 5, 15, 30, 70, 140, 999]

    @property
    def rain_24h(self) -> list:
        """24小时累积降雨阈值 [-5, 0, 15, 35, 100]"""
        return [0, 0.1, 10, 25, 50, 100, 250, 999]

    rain_level = {"1": "small", "2": "mid", "3": "big", "4": "storm"}

    @property
    def snow_1h(self) -> list:
        """1小时累积降雪阈值 [0, 0.1, 0.2, 0.5, 0.7, 100]"""
        return [0, 0.1, 0.2, 0.5, 0.7, 100]

    @property
    def snow_3h(self) -> list:
        """3小时累积降雪阈值 [0, 0.1, 0.3, 0.6, 1.5, 100]"""
        return [0, 0.1, 0.3, 0.6, 1.5, 100]

    @property
    def snow_6h(self) -> list:
        """6小时累积降雪阈值 [0, 0.1, 0.5, 1.5, 3.0, 100]"""
        return [0, 0.1, 0.5, 1.5, 3.0, 100]

    @property
    def snow_12h(self) -> list:
        """12小时累积降雪阈值 [0, 0.1, 1, 3, 6, 100]"""
        return [0, 0.1, 1, 3, 6, 100]

    @property
    def snow_24h(self) -> list:
        """24小时累积降雪阈值 [0, 0.1, 2.5, 5, 10, 100]"""
        return [0, 0.1, 2.5, 5, 10, 100]


class GRIB2DICT(object):
    PRE_1h = dict(parameterName="Total precipitation")
    rain = dict(parameterName="Total precipitation", level=0, stepType="instant"),
    tp = dict(parameterName="Total precipitation", level=0, stepType="accum"),
    tem = dict(parameterName="Temperature", level=2, stepType="instant"),
    sp = dict(parameterName="Pressure", level=0, stepType="instant"),
    rhu = dict(parameterName="Relative humidity", level=2, stepType="instant"),
    u = dict(parameterName="u-component of wind", level=10, stepType="instant"),
    v = dict(parameterName="v-component of wind", level=10, stepType="instant"),
