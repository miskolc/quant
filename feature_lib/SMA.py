import pandas as pd


# Simple Moving Average 
'''
Daily Closing Prices: 11,12,13,14,15,16,17
First day of 5-day SMA: (11 + 12 + 13 + 14 + 15) / 5 = 13
'''
def SMA(data, ndays): 
    SMA = pd.Series(pd.rolling_mean(data['close'], ndays), name = 'SMA') 
    data = data.join(SMA) 
    return data

