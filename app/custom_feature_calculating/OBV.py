import tushare as ts
import pandas as pd
import talib
import numpy as np

'''
http://wiki.mbalib.com/wiki/%E8%83%BD%E9%87%8F%E6%BD%AE%E6%8C%87%E6%A0%87
能量潮指标（On Balance Volume，OBV）是葛兰维（Joe Granville）于本世纪60年代提出的，并被广泛使用。
股市技术分析的四大要素：价、量、时、空。OBV指标就是从“量”这个要素作为突破口，来发现热门股票、分析股价运动趋势的一种技术指标。
它是将股市的人气——成交量与股价的关系数字化、直观化，以股市的成交量变化来衡量股市的推动力，
从而研判股价的走势。关于成交量方面的研究，OBV能量潮指标是一种相当重要的分析指标之一。
'''


def fill(df):
    real = talib.OBV(df["close"].values, df["volume"].values)
    obv = pd.Series(real, name="obv")
    df = df.join(obv)

    return df

if __name__ == "__main__":
    df = ts.get_k_data('600179')

    df = fill(df)

    print(df)
