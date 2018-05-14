# coding=utf-8
import tushare as ts
from sklearn import preprocessing

import app.custom_feature_calculating.K_w_R_rate as w_R_rate
from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.K_uos import uos
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.MACD as macd
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier
import warnings
import numpy as np

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
    return df


features = ['close', 'low', 'high', 'volume', 'open', 'ma5', 'ma10', 'ma20', 'ubb', 'macd'
    , 'lbb', 'ewma', 'evm'
    , 'wr14', 'wr10', 'wr28', 'uos']


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


def predict(code):
    X_pred = predict_data(code)
    X, y = prepare_data(code, ktype='D')



    lg = LogisticRegression()
    lg_scores = cross_val_score(lg, X, y, cv=10)
    # 最小样本测试
    param_test_min = {'min_samples_split': range(80, 130, 20), 'min_samples_leaf': range(10, 60, 10)}
    gsearch_min = GridSearchCV(estimator=RandomForestClassifier(n_estimators=1000, max_depth=3,
                                                                max_features='sqrt', oob_score=True, random_state=10),
                               param_grid=param_test_min, scoring='roc_auc', iid=False, cv=5, n_jobs=-1)

    gsearch_min.fit(X, y)

    # SVC
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]
    # Perform the grid search on the tuned parameters
    gsearch_svc = GridSearchCV(SVC(C=1), tuned_parameters, cv=10, n_jobs=-1)
    gsearch_svc.fit(X, y)

    # LinearSVC
    lsvc = LinearSVC()
    lsvc_scores = cross_val_score(lsvc, X, y, cv=10)

    #XGBClassifier
    # xgb_model = XGBClassifier(n_estimators=1000, n_jobs=-1)
    # parameters = {'learning_rate': [0.01, 0.02, 0.03], 'max_depth': [4, 5, 6]}
    # xgb_search = GridSearchCV(xgb_model, parameters, scoring='roc_auc')
    # xgb_search.fit(X, y)


    models = [("LR", lg, lg_scores.mean()),
              ("RF", gsearch_min.best_estimator_, gsearch_min.best_score_),
              ("SVC", gsearch_svc.best_estimator_, gsearch_svc.best_score_),
              ("LSVC", lsvc, lsvc_scores.mean()),
              # ("XGB", xgb_search.best_estimator_, xgb_search.best_score_),
              ]

    pred_list = []
    # with open('/Users/yw.h/Documents/hs300-selection-result.log', 'a', encoding='utf8') as f:
    for m in models:
        m[1].fit(X, y)
        y_test_pred = m[1].predict(X_pred[-1:])
        print("模型:%s, score:%s, 趋势:%s" % (m[0], m[2], y_test_pred))
        # f.writelines("股票代码: %s 模型:%s, score:%s, 趋势:%s \n" % (code, m[0], m[2], y_test_pred))
        pred_list.append(y_test_pred[0])

    return pred_list


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    code = input("Enter the code: ")
    if not code.strip():
        code = '600179'

    predict(code)
