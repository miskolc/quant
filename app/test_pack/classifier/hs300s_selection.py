#coding=utf-8
import time

import datetime
import tushare as ts

from app.test_pack.classifier.classifier_runner import predict
import warnings



def vote(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 1


def filter(codes):
    print(codes)
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
        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(repr(e))

    return list


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    rs = classifier_predict(ts.get_hs300s())

    rs = filter(rs)

    print(rs)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(duration)