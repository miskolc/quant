
import pandas as pd

# Commodity Channel Index 
'''
CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)
Typical Price (TP) = (High + Low + Close)/3
Constant = .015
'''
def CCI(data, ndays): 
    TP = (data['high'] + data['low'] + data['close']) / 3 
    CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015 * pd.rolling_std(TP, ndays)),
    name = 'cci') 
    data = data.join(CCI) 
    return data