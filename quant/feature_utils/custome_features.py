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


def cal_turnover(data):
    turn_over = data['volume'] / 100 / data['share_oustanding']
    return turn_over


def cal_PHLambdaT(data):
    t_price_open = data['open']
    t_minue_one_open = data['open'].shift(1)
    max_21_price_high = pd.Series.rolling(data['high'], 21).max()
    max_21_price_low = pd.Series.rolling(data['low'], 21).min()

    PHLambdaT = (t_price_open - t_minue_one_open) / (max_21_price_high - max_21_price_low)

    return PHLambdaT


def cal_VHLambdaT(data):
    t_vol = data['volume']
    t_minus_one = data['volume'].shift(1)
    max_21_vol_high = pd.Series.rolling(data['volume'], 21).max()
    max_21_vol_low = pd.Series.rolling(data['volume'], 21).min()

    VHLambdaT = (t_vol - t_minus_one) / (max_21_vol_high - max_21_vol_low)

    return VHLambdaT
