# ae.h - 2018/5/20
from talib import abstract


def cal_bbands(data):
    bbands_func = abstract.Function('bbands')
    bbands = bbands_func(data)
    return bbands


def cal_dema(data):
    dema_func = abstract.Function('dema')
    dema = dema_func(data)
    return dema


def cal_ema(data, period=30):
    ema_func = abstract.Function('ema')
    ema = ema_func(data, timeperiod=period, price='close')
    return ema


# period 20
def cal_ht_trendline(data):
    ht_trend_line_func = abstract.Function('ht_trendline')
    ht_trend_line = ht_trend_line_func(data, price='close')
    return ht_trend_line


def cal_kama(data):
    kama_func = abstract.Function('kama')
    kama = kama_func(data, price='close')
    return kama


def cal_ma5(data):
    ma_func = abstract.Function('ma')
    ma5 = ma_func(data, timeperiod=5, price='close')
    return ma5


def cal_ma10(data):
    ma_func = abstract.Function('ma')
    ma10 = ma_func(data, timeperiod=10, price='close')
    return ma10


def cal_ma20(data):
    ma_func = abstract.Function('ma')
    ma20 = ma_func(data, timeperiod=20, price='close')
    return ma20

def cal_ma30(data):
    ma_func = abstract.Function('ma')
    ma30 = ma_func(data, timeperiod=30, price='close')
    return ma30

def cal_ma60(data):
    ma_func = abstract.Function('ma')
    ma60 = ma_func(data, timeperiod=60, price='close')
    return ma60

def cal_ma145(data):
    ma_func = abstract.Function('ma')
    ma60 = ma_func(data, timeperiod=145, price='close')
    return ma60

def cal_mama(data):
    mama_func = abstract.Function('mama')
    mama = mama_func(data, price='close')
    return mama


# def cal_mavp(data, period=5):
#     mavp_func = abstract.Function('mavp')
#     mavp = mavp_func(data, timeperiod=period)
#     return mavp


def cal_midpoint(data, period=14):
    midpoint_func = abstract.Function('midpoint')
    midpoint = midpoint_func(data, timeperiod=period)
    return midpoint


def cal_midprice(data, period=14):
    midprice_func = abstract.Function('midprice')
    midprice = midprice_func(data, timeperiod=period)
    return midprice


def cal_sar(data):
    sar_func = abstract.Function('sar')
    sar = sar_func(data)
    return sar


def cal_sarext(data):
    sarext_func = abstract.Function('sarext')
    sarext = sarext_func(data)
    return sarext


def cal_sma(data, period=5):
    sma_func = abstract.Function('sma')
    sma = sma_func(data, timeperiod=period)
    return sma


def cal_t3(data, period=5):
    t3_func = abstract.Function('t3')
    t3 = t3_func(data, timeperiod=period)
    return t3


def cal_trima(data, period=30):
    trima_func = abstract.Function('trima')
    trima = trima_func(data, timeperiod=period)
    return trima


def cal_wma(data, period=30):
    wma_func = abstract.Function('wma')
    wma = wma_func(data, timeperiod=period)
    return wma
