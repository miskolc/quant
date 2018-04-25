import pandas as pd



def fill(data):
    EMA12 = pd.Series(pd.Series.ewm(data['close'], span=12).mean(),
                    name='ewma12')
    EMA26 = pd.Series(pd.Series.ewm(data['close'], span=12).mean(),
                    name='ewma26')

    MACD = pd.Series(EMA12 - EMA26, name='macd')

    pass