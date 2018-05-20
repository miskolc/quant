# ae.h - 2018/5/20
from talib import abstract
import pandas as pd
import numpy as np


def cal_ema(data, period):
    ema_func = abstract.Function('ema')
    ema = ema_func(data, timeperiod=period, price='close')
    return ema


# default 20 days
# nbdevup=2.0
# nbdevdn=2.0
def cal_bbands(data):
    bbands_func = abstract.Function('bbands')
    bbands = bbands_func(data, 20, 2, 2)
    return bbands


