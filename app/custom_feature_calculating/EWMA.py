import pandas as pd


# EWMA Exponentially-weighted Moving Average - 指数加权移动平均
def EWMA(data, ndays):
    EMA = pd.Series(pd.Series.ewm(data['close'], span=ndays, min_periods=ndays).mean(),
                    name='ewma')
    data = data.join(EMA)
    return data
