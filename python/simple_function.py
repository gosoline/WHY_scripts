from datetime import datetime

import pandas as pd


def get_month_FL(
    date: str | pd.Timestamp | datetime,
    n: int,
) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Parameters
    -----------
    ~:获取上n个月的月初和月末日期, 其中n为负数表示获取上n个月的日期, 正数表示获取下n个月的日期, 0表示获取当前月的日期.
    - date: str | pd.Timestamp | datetime, 日期
    - n: int, 月份数量

    Returns
    --------
    tuple[pd.Timestamp, pd.Timestamp], 返回一个元组, 第一个元素为上n个月的月初日期, 第二个元素为上n个月的月末日期
    """
    date: pd.Timestamp = pd.to_datetime(date)

    first_day_of_last_month = pd.Timestamp(
        year=date.year, month=date.month, day=1) + pd.offsets.MonthBegin(n)
    last_day_of_last_month = first_day_of_last_month + pd.offsets.MonthEnd(1)
    return first_day_of_last_month, last_day_of_last_month
