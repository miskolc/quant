# ae.h - 2018/4/28

import pandas as pd
import numpy as np
import tushare as ts
from sklearn import svm
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score


def svc_classifier():
    df = ts.bar('600179', freq='5min', start_date='2016-01-01', end_date='2017-10-10', conn=ts.get_apis())
    df['price_change'] = df['close'] - df['close'].shift(-1)
    df['direction'] = np.where(df['price_change'] > 0, 1, 0)
    df['direction'] = df['direction'].shift(-1)
    df = df.dropna()

    X = df[['open', 'close', 'high', 'low', 'vol', 'amount', 'price_change']]
    y = df['direction'].values.ravel()

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

    print(X.shape)
    print(y.shape)
    svc_model = svm.SVC(kernel='rbf')

    svc_model.fit(X, y)

    cv_results = cross_validate(svc_model, X, y, cv=10, n_jobs=-1)

    cv_score = cross_val_score(svc_model, X, y, cv=10, n_jobs=-1)

    print('train_score: %s \n' % cv_results['train_score'])

    print('test_score: %s \n' % cv_results['test_score'])

    print('cv_score: %s \n' % cv_score)

    ts.close_apis(conn=ts.get_apis())


if __name__ == '__main__':
    svc_classifier()
