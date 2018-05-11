# coding=utf-8
import warnings

import tushare as ts
from sklearn import preprocessing

import app.custom_feature_calculating.K_w_R_rate as w_R_rate
import app.custom_feature_calculating.MACD as macd
from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from app.custom_feature_calculating.K_uos import uos
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.RSI as RSI
from app.custom_feature_calculating.CCI import CCI
import app.custom_feature_calculating.OBV as OBV
import app.custom_feature_calculating.ROC as ROC
import app.custom_feature_calculating.KDJ as KDJ
from app.custom_feature_calculating.FI import ForceIndex


def f(x):
    if x > 0:
        return 1
    else:
        return 0


def fill_feature(df):
    df = SMA(df, 20)
    df = SMA(df, 10)
    df = SMA(df, 5)
    df = BBANDS(df, 20)
    df = w_R_rate.w_R_rate(df, 10)
    df = w_R_rate.w_R_rate(df, 14)
    df = w_R_rate.w_R_rate(df, 28)
    df = uos(df)
    df = macd.fill(df)
    df = EMV(df, 5)
    df = EWMA(df, 5)
    df = RSI.fill(df)
    df = CCI(df, 14)
    df = OBV.fill(df)
    df = ROC.fill(df)
    df = KDJ.fill(df)
    df = ForceIndex(df, 1)
    df = ForceIndex(df, 13)
    return df


features = ['close', 'low', 'high', 'volume', 'open', 'ma5', 'ma10', 'ma20', 'ubb','lbb', 'macd'
           , 'ewma', 'evm', 'wr14', 'wr10', 'wr28', 'uos','rsi6','rsi12','rsi24','cci','obv', 'roc','slowk','slowd', 'fi1' ,'fi13']


def prepare_data(code, ktype='D'):
    df = ts.get_k_data(code, ktype=ktype)
    df = fill_feature(df)
    # df['direction'] = df['p_change'] > 0
    df['pre_close'] = df['close'].shift();
    df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
    df['price_change'] = df['close'] - df['pre_close']
    # df['direction'] = np.where(df['price_change'] > 0, 1, 0)
    df['direction'] = df['p_change'].shift(-1).apply(f)
    df = df.dropna()
    df.to_csv('result.csv')
    X = df[features].values

    y = df[["direction"]].values.ravel()

    X = preprocessing.normalize(X)
    return X, y


def predict_data(code, ktype='D'):
    df = ts.get_k_data(code, ktype=ktype)
    df = fill_feature(df)

    df = df.dropna();

    print("股票代码:%s, close price:%s" % (code, df[-1:]["close"].values))

    X = df[features].values

    X = preprocessing.normalize(X)
    return X