# ae.h - 2018/5/4
# coding=utf-8

# coding=utf-8

import tushare as ts
import pandas as pd
import numpy as np
from app.test_pack.classifier.classifier_runner import predict
from googlefinance.client import get_price_data
import app.custom_feature_calculating.MACD as MACD
import app.custom_feature_calculating.SMA as SMA


def vote(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 0.8


def filter(codes):
    list = []
    for code in codes:
        df_sh = ts.get_hist_data(code)

        if df_sh is None:
            continue

        date = df_sh.index.values[0]
        if date < '2018-05-04':
            continue

        close = df_sh["close"].head(1).values[0]
        ma5 = df_sh["ma5"].head(1).values[0]
        ma10 = df_sh["ma10"].head(1).values[0]
        ma20 = df_sh["ma20"].head(1).values[0]
        if close > ma5 and close > ma10 and close > ma20:
            list.append(code)
    return list


def classifier_predict(df):
    list = []
    for code in df['code'].values:
        pred_result = predict(code)
        print(pred_result)
        rs = vote(pred_result)
        if rs is True:
            list.append(code)

    return list


if __name__ == "__main__":

    # rs = classifier_predict(ts.get_hs300s())
    #
    # rs = filter(rs)
    #
    # print(rs)


    sp_df = pd.read_csv('/Users/yw.h/Documents/sp500_selection.csv')

    print(sp_df)
    for code in sp_df['code'].values:
        param = {
            'q': code,  # Stock symbol (ex: "AAPL")
            'i': "86400",  # Interval size in seconds ("86400" = 1 day intervals)
            'p': "%sY" % '5'  # Period (Ex: "1Y" = 1 year)
        }
        # get price data (return pandas dataframe)
        sp_df = get_price_data(param)
        # rename columns to lowercase/Users/yw.h/quant-awesome/app/test_pack/classifier/sp500_selection.py
        sp_df = sp_df.rename(
            columns={"Code": "code", "Open": "open", "High": "high", "Low": "low", "Close": "close",
                     "Volume": "volume"})

    sp_df = MACD.fill(sp_df, 'close')
    sp_df = SMA.SMA(sp_df, 5)
    sp_df = SMA.SMA(sp_df, 10)
    sp_df = SMA.SMA(sp_df, 20)

    rs = classifier_predict(sp_df)
    rs = filter(rs)
    print(rs)
