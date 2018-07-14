# coding = utf-8
# ae.h - 2018/5/28

from talib import abstract


def cal_atr(data):
    atr_func = abstract.Function('atr')
    atr = atr_func(data)
    return atr

def cal_natr(data):
    natr_func = abstract.Function('natr')
    natr = natr_func(data)
    return natr

def cal_trange(data):
    trange_func = abstract.Function('trange')
    trange = trange_func(data)
    return trange