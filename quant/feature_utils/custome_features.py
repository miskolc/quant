# coding = utf-8
# ae.h - 2018/5/28

from talib import abstract
import pandas as pd
import numpy as np
import tushare as ts

#
def cal_mavol5(data):
    mavol5 = pd.rolling_sum(data['volume'], 5)/5
    return mavol5


def cal_mavol10(data):
    mavol10 = pd.rolling_sum(data['volume'], 10)/10
    return mavol10

def cal_mavol20(data):
    mavol20 = pd.rolling_sum(data['volume'], 20)/20
    return mavol20


