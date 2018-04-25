import pandas as pd
import tushare as ts


# The MACD Line is the 12-day Exponential Moving Average (EMA) less the 26-day EMA
# MACD Line: (12-day EMA - 26-day EMA)
# https://zh.wikipedia.org/wiki/MACD
def fill(data):
    EMA12 = pd.Series(pd.Series.ewm(data['close'], span=12).mean(),
                      name='ewma12')
    EMA26 = pd.Series(pd.Series.ewm(data['close'], span=26).mean(),
                      name='ewma26')

    MACD = pd.Series(EMA12 - EMA26, name='macd')
    data = data.join(MACD)
    return data


if __name__ == "__main__":
    df = ts.get_hist_data('600179')
    df = fill(df)

    print(df)
    pass
