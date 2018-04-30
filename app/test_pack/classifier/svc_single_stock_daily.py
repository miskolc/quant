import tushare as ts
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import app.custom_feature_calculating.K_w_R_rate as w_R_rate
from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.K_uos import uos
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.MACD as macd
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from sklearn.model_selection import cross_val_score


def f(x):
    if x > 0:
        return 1

    elif x < 0:
        return -1
    else:
        return 0


'''


def f(x):
    if 0.01 > x > 0:
        return 'U001'
    elif 0.05 > x > 0.01:
        return 'U002'
    elif 0.05 < x:
        return 'U003'
    elif -0.01 < x < 0:
        return 'D001'
    elif -0.05 < x < -0.01:
        return 'D002'
    elif -0.05 > x:
        return 'D003'
    elif x == 0:
        return 'E000'
    else:
        return None
'''


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


features = ["close", "low", "high", "volume", 'ma5', 'ma10', 'ma20', 'ubb', 'macd'
    , 'lbb', 'ewma', 'evm'
    , 'wr14', 'wr10', 'wr28', 'uos']


def prepare_data(code, start, end, ktype='5'):
    df = ts.get_k_data(code, start=start, end=end, ktype=ktype)
    df = fill_feature(df)
    # df['direction'] = df['p_change'] > 0
    df['pre_close'] = df['close'].shift();
    df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
    df['price_change'] = df['close'] - df['pre_close']
    # df['direction'] = np.where(df['price_change'] > 0, 1, 0)
    df['direction'] = df['p_change'].shift(-1).apply(f)
    df = df.dropna()
    df.to_csv('result_%s_%s.csv' % (start, end))
    X = df[features]

    y = df[["direction"]].values.ravel()

    # X = preprocessing.normalize(X)
    return X, y


def prepare_daily_data_from_db(code, start, end):
    pass


def predict_data(code, start, end, ktype='5'):
    df = ts.get_k_data(code, start=start, end=end, ktype=ktype)
    df = fill_feature(df)
    X = df[features]

    # X = preprocessing.normalize(X)
    return X


def train():
    pass


def predit():
    pass


if __name__ == "__main__":
    code = '600179'
    X, y = prepare_data(code, '2015-01-01', '2018-04-27', ktype='D')

    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]
    # Perform the grid search on the tuned parameters
    model = GridSearchCV(SVC(C=1), tuned_parameters, cv=10, n_jobs=-1)
    model.fit(X, y)

    print("Optimised parameters found on training set:")
    print(model.best_estimator_, "\n")

    svc = model.best_estimator_

    # svc.fit(X_train, y_train)
    #svc.fit(X, y)
    print(model.best_score_, "\n")

    #scores = cross_val_score(svc, X, y, cv=10, scoring='accuracy')
    #print(scores)

    #X, y = prepare_data(code, '2018-01-02', '2018-04-26', ktype='D')
    #print(svc.score(X, y))


    X = predict_data(code, '2018-01-26', '2018-04-27', ktype='D')
    print(X[-1:])
    y_test_pred = svc.predict(X[-1:])
    print(y_test_pred)

