# -*- coding: utf-8 -*-
"""
@File    : value_at.py
@Time    : 2024/05/13 08:57:18
@Author  : WHY
@Version : 1.0
@Desc    : None
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import pandas as pd

__all__ = ['get_decimal_places', 'values_at']


def get_decimal_places(number: float) -> int:
    '''
    ~:获取数字小数位数
    
    Parameters
    ----------
    - number: float, 数字
    '''
    number_str = str(number)
    parts = number_str.split('.')
    if len(parts) == 1:
        decimal_places = 0
    else:
        decimal_places = len(parts[-1])
    return decimal_places


def values_at(
    values: float | pd.Timestamp | Iterable[float | pd.Timestamp],
    interval_size: float | pd.Timedelta,
    label_point: float | pd.Timestamp = None,
    is_time: bool = None,
    label_loc: float = None,
    format: str = None,
) -> float | pd.Timestamp | list[float | pd.Timestamp]:
    '''
    ~:获取值(数字或时间)所在区间

    Parameters
    ----------
    - values: float | pd.Timestamp | Iterable[float | pd.Timestamp], 值或值迭代对象
    - interval_size: float | pd.Timedelta, 区间大小
    - label_point: float | pd.Timestamp = None, 可存在的标签点
    - is_time: bool = None, 是否为时间类型,默认自动判断
    - label_loc: float = None, 标签点在区间的位置,为`None`时数字为`0.5`,时间为`0`
    - format: str = None, 时间格式

    Returns
    -------
    - float | pd.Timestamp | list[float | pd.Timestamp], 值所在区间
    '''
    if isinstance(values, str):
        iterable_ = False
    else:
        iterable_ = isinstance(values, Iterable)

    values = pd.Series(values).reset_index(drop=True)

    if values.shape[0] > 0:
        if is_time is None:
            if isinstance(values.iloc[0], (str, pd.Timedelta, datetime)):
                is_time = True
            else:
                is_time = False
    else:
        return values.to_list()

    if label_point is None:
        label_point = 0
    if label_loc is None:
        if is_time:
            label_loc = 0
        else:
            label_loc = 0.5
    if is_time:
        values = (pd.to_datetime(values, format=format) -
                  pd.to_datetime(0)).apply(pd.Timedelta.total_seconds)
        interval_size = pd.to_timedelta(interval_size).total_seconds()
        label_point = (pd.to_datetime(label_point) -
                       pd.to_datetime(0)).total_seconds()

    values_at_: pd.Series | float = (
        (values - label_point + interval_size * label_loc) //
        interval_size) * interval_size + label_point

    decimal_list = []
    # decimal_list.append(values.apply(get_decimal_places).max())
    decimal_list.append(get_decimal_places(interval_size * label_loc))
    decimal_list.append(get_decimal_places(label_point))

    values_at_ = values_at_.round(max(decimal_list))
    if is_time:
        values_at_ = pd.to_datetime(values_at_, unit='s')
    values_at_ = values_at_.to_list()

    return values_at_ if iterable_ else values_at_[0]


if __name__ == '__main__':
    values_at_ = values_at(
        [2.54, 2.3, 2.56, 2.04, 2.06],
        0.5,
        # label_point=2.3,
        # label_loc=0.5,
    )
    print(values_at_)
    values_at_ = values_at(
        '2023/1/14 11:14:50',
        '1d',
        # label_point='2023/1/11 11:00:00',
        label_loc=0.5,
    )
    print(values_at_)
