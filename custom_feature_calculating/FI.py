import pandas as pd


# FI Force Index - 力量指数
'''
Force Index(1) = {Close (current period)  -  Close (prior period)} x Volume
Force Index(13) = 13-period EMA of Force Index(1)
'''

def ForceIndex(data, ndays):
    FI = pd.Series(data['close'].diff(ndays) * data['volume'], name='fi')
    data = data.join(FI)
    return data
