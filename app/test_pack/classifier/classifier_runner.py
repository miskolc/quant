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
    X = df[features]

    y = df[["direction"]].values.ravel()

    X = preprocessing.normalize(X)
    return X, y


def predict_data(code, ktype='D'):
    df = ts.get_k_data(code, ktype=ktype)
    df = fill_feature(df)
    X = df[features]

    return X


def predict(code):
    X_pred = predict_data(code)
    X, y = prepare_data(code, ktype='D')

    print("股票代码:%s, close price:%s" % (code, X_pred[-1:]["close"].values))

    lg = LogisticRegression()
    lg_scores = cross_val_score(lg, X, y, cv=10)
    # RandomForestClassifier 弱网格测试
    param_test_weak = {'n_estimators': range(100, 500, 100)}
    gsearch_weak = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,n_jobs=-1,
                                                                 min_samples_leaf=20, max_depth=8, max_features='sqrt',
                                                                 random_state=10),
                                param_grid=param_test_weak, scoring='roc_auc', cv=5)

    gsearch_weak.fit(X, y)

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

    models = [("LR", lg, lg_scores.mean()),
              ("RF", gsearch_weak.best_estimator_, gsearch_weak.best_score_),
              ("SVC", gsearch_svc.best_estimator_, gsearch_svc.best_score_),
              ("LSVC", lg, lsvc_scores.mean()),
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

    code = input("Enter the code: ")
    if not code.strip():
        code = '600179'

    predict(code)
