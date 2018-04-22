import pandas as pd

# CCI Commodity Channel Index - 顺势指标
'''
CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)
Typical Price (TP) = (High + Low + Close)/3
Constant = .015
'''


def CCI(data, ndays):
    TP = (data['high'] + data['low'] + data['close']) / 3
    CCI = pd.Series((TP - pd.Series.rolling(TP, ndays).mean()) / (0.015 * pd.Series.rolling(TP, ndays).std()),
                    name='cci')
    data = data.join(CCI)
    return data
