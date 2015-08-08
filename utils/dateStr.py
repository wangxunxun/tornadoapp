#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time

def _ch_d(_d_n):
    _d_n = int(_d_n)
    if _d_n == 1:
        return "一"
    elif _d_n == 2:
        return "二"
    elif _d_n == 3:
        return "三"
    elif _d_n == 4:
        return "四"
    elif _d_n == 5:
        return "五"
    elif _d_n == 6:
        return "六"
    elif _d_n == 7:
        return "日"
    else:
        return "八"

def get_week_str(d=None):
    if d is None:
        d = datetime.datetime.now()

    _d = d.isocalendar()[2]

    return "周" + _ch_d(_d)


def get_hour_minute_str(d=None):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    _h = d.hour
    _m = d.minute
    if _h < 10:
        _h = "0" + str(_h)
    if _m < 10:
        _m = "0" + str(_m)
    _str = str(_h) + ":" + str(_m)
    return _str

def get_hour_minute_second_str(d=None):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    _h = d.hour
    _m = d.minute
    _s = d.second
    if _h < 10:
        _h = "0" + str(_h)
    if _m < 10:
        _m = "0" + str(_m)
    if _s < 10:
        _s = "0" + str(_s)
    _str = str(_h) + ":" + str(_m) + ":" + str(_s)
    return _str

def get_year_week_day_str(d=None):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    d = d.isocalendar()
    _y = d[0]
    _w = d[1]
    _d = d[2]
    if _y < 10:
        _y = "0" + str(_y)
    if _w < 10:
        _w = "0" + str(_w)
    _str = str(_y) + "-" + str(_w) + "-" + str(_d)
    return _str

def get_year_week_day_str_ch(d=None):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    d = d.isocalendar()
    _y = d[0]
    _w = d[1]
    _d = d[2]
    if _y < 10:
        _y = "0" + str(_y)
    if _w < 10:
        _w = "0" + str(_w)
    _str = str(_y) + "年 第" + str(int(_w)) + "周 周" + _ch_d(_d)
    return _str

def get_year_week_day_str_ch_from_format_str(s):
    d=s.split("-")
    _y = int(d[0])
    _w = int(d[1])
    _d = int(d[2])
    if _y < 10:
        _y = "0" + str(_y)
    if _w < 10:
        _w = "0" + str(_w)
    _str = str(_y) + "年 第" + str(int(_w)) + "周 周" + _ch_d(_d)
    return _str

def get_year_week_str(d=None):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    d = d.isocalendar()
    _y = d[0]
    _w = d[1]
    if _y < 10:
        _y = "0" + str(_y)
    if _w < 10:
        _w = "0" + str(_w)
    _str = str(_y) + "-" + str(_w)
    return _str

def get_year_month_day_str(d=None, s="-"):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    _y = d.year
    _m = d.month
    _d = d.day
    if _y < 10:
        _y = "0" + str(_y)
    if _m < 10:
        _m = "0" + str(_m)
    if _d < 10:
        _d = "0" + str(_d)
    _str = str(_y) + s + str(_m) + s + str(_d)
    return _str

def get_year_month_day_str_ch(d=None, s="-"):
    if d is not None:
        d = d
    else:
        d = datetime.datetime.now()
    _y = d.year
    _m = d.month
    _d = d.day
    if _y < 10:
        _y = "0" + str(_y)
    if _m < 10:
        _m = "0" + str(_m)
    if _d < 10:
        _d = "0" + str(_d)
    _str = str(int(_y)) + "年" + str(int(_m)) + "月" + str(int(_d)) + "日"
    return _str

if __name__ == '__main__':
    print get_year_month_day_str_ch()
    print get_hour_minute_str()
    print get_hour_minute_second_str()
    print get_year_week_day_str()
    print get_year_month_day_str()
    print get_year_week_str()
    print get_year_week_day_str_ch()
    print get_year_week_day_str_ch_from_format_str(get_year_week_day_str())