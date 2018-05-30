# coding=utf-8

import warnings

import tushare as ts

from app.test_pack.backup.rf.hs300s.classifier_runner import predict
from app.custom_feature_calculating.SMA import SMA

def vote8(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 0.8


def vote100(list):
    count = 0.0
    for item in list:
        if item == 1:
            count += 1

    return count / len(list) >= 1


def filter(codes):
    print(codes)
    list = []
    for code in codes:

        df_rel = ts.get_k_data(code)

        if df_rel is None:
            continue


        df_rel = SMA(df_rel, 10)
        df_rel = SMA(df_rel, 20)

        df_rel = df_rel.tail(1)


        ma10 = df_rel["ma10"].values[0]
        ma20 = df_rel["ma20"].values[0]

        price = float(ts.get_realtime_quotes(code)["price"].values[0])

        if price > ma10 and price > ma20:
            list.append(code)

        '''
        pre_price = float(df_rel["pre_close"].tail(1).values[0])
        price = float(df_rel["price"].tail(1).values[0])

        p_change = (price - pre_price) / pre_price
        print(p_change)
        if p_change < -0.02:
            list.append(code)
            print(p_change)
        '''
    return list


def classifier_predict8(df):
    list = []
    for code in df['code'].values:
        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote8(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(e)
    return list


def classifier_predict100(df):
    list = []
    for code in df['code'].values:
        try:
            pred_result = predict(code)
            print(pred_result)
            rs = vote100(pred_result)
            if rs is True:
                list.append(code)
        except Exception as e:
            print(e)
    return list


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    rs = classifier_predict100(ts.get_hs300s())
    rs = filter(rs)

    print(rs)

    #rs = classifier_predict8(ts.get_hs300s())

    #rs = filter(rs)

    #print(rs)
