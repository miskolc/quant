# ae.h - 2018/4/28

import pandas as pd
import tushare as ts
from sklearn import svm
from sklearn.model_selection import cross_validate, cross_val_score, GridSearchCV, train_test_split
from timeit import Timer


def svc_classifier():
    # df = ts.bar('600179', freq='5min', start_date='2016-01-01', end_date='2017-10-10', conn=ts.get_apis())
    # df['price_change'] = df['close'] - df['close'].shift(-1)
    # df['direction'] = np.where(df['price_change'] > 0, 1, 0)
    # df['direction'] = df['direction'].shift(-1)
    # df = df.dropna()

    df = pd.read_csv('/Users/yw.h/Downloads/result.csv')

    X = df[['open', 'close', 'high', 'low', 'volume', 'ma20', 'ma10', 'ma5', 'ubb', 'lbb', 'wr10', 'wr14', 'wr28', 'uos', 'macd', 'evm', 'ewma', 'pre_close', 'p_change', 'price_change']]
    y = df['direction'].values.ravel()

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

    print(X.shape)
    print(y.shape)

    # tuned_parameters = [
    #     {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    # ]
    # # Perform the grid search on the tuned parameters
    # model = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=10)
    # model.fit(X_train, y_train)
    #
    # print("Optimised parameters found on training set:")
    # print(model.best_estimator_, "\n")
    #
    # svc = model.best_estimator_

    svc_model = svm.SVC(kernel='rbf')

    svc_model.fit(X, y)

    cv_results = cross_validate(svc_model, X, y, cv=10, n_jobs=-1)

    # cv_score = cross_val_score(svc_model, X, y, cv=10, n_jobs=-1)

    print('train_score: %s \n' % cv_results['train_score'])

    print('test_score: %s \n' % cv_results['test_score'])

    # print('cv_score: %s \n' % cv_score)

    ts.close_apis(conn=ts.get_apis())


if __name__ == '__main__':
    t1 = Timer("svc_classifier()", "from __main__ import svc_classifier")
    svc_classifier()
    print(t1)
