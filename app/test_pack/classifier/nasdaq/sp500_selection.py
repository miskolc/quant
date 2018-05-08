# ae.h - 2018/5/4
# coding=utf-8

# coding=utf-8

import pandas as pd
import tushare as ts

from app.test_pack.classifier.nasdaq.classifier_runner import predict


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


def classifier_predict():

    sp_df = pd.read_csv('sp500_selection.csv')

    list = []
    for code in sp_df['code'].values:

        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(e)


    return list


if __name__ == "__main__":

    # rs = classifier_predict(ts.get_hs300s())
    #
    # rs = filter(rs)
    #
    # print(rs)

    rs = classifier_predict()
    #rs = filter(rs)
    print(rs)
