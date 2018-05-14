import pandas as pd
import tushare as ts
import talib

'''
Stochastic Oscillator Slow （Stoch）更直接的理解就是我们常用的KDJ指标中的KD指标。
是由两条线一条是快速确认线，另外一条是慢速主干线组成

使用方法：
K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；
D线是慢速主干线——数值在90以上为超买，数值在10以下为超卖；

'''


def fill(df):
    slowk, slowd = talib.STOCH(df['high'],
                               df['low'],
                               df['close'],
                               fastk_period=9,
                               slowk_period=3,
                               slowk_matype=0,
                               slowd_period=3,
                               slowd_matype=0)

    k = pd.Series(slowk, name='slowk')
    d = pd.Series(slowd, name='slowd')
    df = df.join(k)
    df = df.join(d)
    return df


if __name__ == "__main__":
    df = ts.get_k_data('600179')

    df = fill(df)

    print(df)
