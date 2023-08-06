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

__all__ = ["PathCather"]

from datetime import datetime, timedelta
import glob
from pathlib import Path
import re
from typing import Optional


class PathCather(object):

    @classmethod
    def catch(cls, time: datetime, lead_time: Optional[timedelta], file: str) -> str:
        """ Catch the path within time, lead time and file rule.

        Args:
            time: The time or report time of the file
            lead_time: None of the observation file.However, it is lead time of the forecast file.
            file: The rule of the file within time format.

        Returns:
            The path of file

        Exampls:


            >>> from datetime import datetime, timedelta
            >>> from aprilbox import PathCather
            >>> tag_time = datetime(year=2022, month=7, day=2, hour=4)   # 目标时间
            >>> file1 = "/mnt/PRESKY/data/cmadata/NAFP/CMPAS_GRIB/%Y/%Y%m/%Y%m%d/*%Y%m%d%H.GRB2"
            >>> file2 = "~/product/FCST/SZW_1000M/F_RADA_FCST_03H_DL/%Y%m%d/F_RADA_FCST_03H_DL_SZW_1000M_%Y%m%d%H%M_%Y%m%d%H%M.nc"

            >>> # 抓取实况时间为 2022年7月2日5时，文件路径规则为file1的实况数据
            >>>path1 = PathCather.catch(time=tag_time + timedelta(hours=1), lead_time=None, file=file1)
            >>> # 抓取起报时间为2022年7月2日4时，预报时间为2022年7月2日5时（预报时效为1小时），文件路径规则为file2的预报产品数据
            >>> path2 = PathCather.catch(time=tag_time, lead_time=timedelta(hours=1), file=file2)
        """
        if file.count("*") > 0:
            # 模糊匹配
            if file.count("%Y") + file.count("%m") + file.count("%d") > 0:
                assert lead_time is None, TypeError(f"{datetime.now()}\n ftime is exists!")
                file = time.strftime(file)
            path = glob.glob(time.strftime(file))
            path = sorted(path, key=lambda x: Path(x).stat().st_ctime, reverse=True)  # 根据文件修改时间进行排序
            if len(path) > 0:
                path = path[0]  # 返回最新修改时间的模糊匹配文件
            else:
                path = file
        else:
            # 精准匹配
            if len(re.findall("{:0\dd}", file)) == 1 and isinstance(lead_time, timedelta):
                # 匹配模式文件名包含预报时长小时数的文件路径
                file = file.format(int(lead_time.total_seconds() / 3600))
            path = cls.merge_file(time, lead_time=lead_time, file=file)
        return path

    @classmethod
    def merge_file(cls, time: datetime, lead_time: Optional[timedelta], file: str) -> str:
        """Merge file path.

        While the file is observation, it will return the file. However, the file is forecast,it will return the file
        merge the report time and forecast time.

        Args:
            time: The time or report time of the file
            lead_time: None of the observation file.However, it is lead time of the forecast file.
            file: The rule of the file within time format.

        Returns:
            The file.
        """
        if lead_time is None:
            # 若预报时长为None，则为实况数据
            return time.strftime(file)
        else:
            # 若预报时长非None，则视time为起报时间
            file_split_1 = time.strftime("_".join(file.split("_")[:-1]))
            file_split_2 = (time + lead_time).strftime(file.split("_")[-1])
            file = file_split_1 + "_" + file_split_2
            return file