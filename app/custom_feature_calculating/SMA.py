import pandas as pd

# Simple Moving Average
'''
 * 简单移动平均线
 * Daily Closing Prices: 11,12,13,14,15,16,17
 * First day of 5-day SMA: (11 + 12 + 13 + 14 + 15) / 5 = 13
'''


def SMA(data, ndays):
    # SMA - Simple Moving Average
    SMA = pd.Series(pd.Series.rolling(data['close'], ndays).mean(), name='ma%s' % ndays)
    data = data.join(SMA)
    return data
