# coding = utf-8
# ae.h - 2018/5/28

from talib import abstract
import pandas as pd
import numpy as np
import tushare as ts


def cal_mavol5(data):
    mavol5 = pd.Series.rolling(data['volume'], 5).sum() / 5
    return mavol5


def cal_mavol10(data):
    mavol10 = pd.Series.rolling(data['volume'], 10).sum() / 10
    return mavol10


def cal_mavol20(data):
    mavol20 = pd.Series.rolling(data['volume'], 20).sum() / 20
    return mavol20


def cal_turnover(vol, share_outstanding):
    turn_over = vol['volume'] / (share_outstanding['share_oustanding'] / 100)
    return turn_over
