import pandas as pd
import tushare as ts


# The MACD Line is the 12-day Exponential Moving Average (EMA) less the 26-day EMA
# MACD Line: (12-day EMA - 26-day EMA)
# https://zh.wikipedia.org/wiki/MACD
def fill(data, col='close'):
    sema = pd.Series(pd.Series.ewm(data[col], span=12).mean(),
                      name='sema')
    lema = pd.Series(pd.Series.ewm(data[col], span=26).mean(),
                      name='lema')

    data_dif = sema - lema
    data_dea = pd.Series(data_dif).ewm(span=9).mean()
    data_macd = 2 * (data_dif - data_dea)

    MACD = pd.Series(data_macd, name='macd')
    data = data.join(MACD)
    return data


if __name__ == "__main__":
    df = ts.get_k_data('600179')
    df.sort_index()
    df = fill(df)

    print(df.head())
    pass
