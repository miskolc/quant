import pandas as pd

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
 EMA = pd.Series(pd.ewma(data['close'], span = ndays, min_periods = ndays - 1), 
 name = 'ewma') 
 data = data.join(EMA) 
 return data