import tushare as ts
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import numpy as np
from sklearn import preprocessing


def train():
    pass


def predit():
    pass


if __name__ == "__main__":
    df = ts.get_hist_data('600179', start='2016-01-01', end='2018-03-01')
    #df['direction'] = df['p_change'] > 0

    df['direction'] =  np.where(df['price_change'] > 0, 1, 0)
    df['direction'] = df['direction'] .shift(-1)
    df = df.dropna()
    X = df[["close","low","high","ma5","ma10", "ma20","v_ma5","v_ma10", "v_ma20", "turnover"]]
    y = df[["direction"]].values.ravel()
    df.to_csv('1.csv')

    X = preprocessing.scale(X)
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]
    # Perform the grid search on the tuned parameters
    model = GridSearchCV(SVC(C=1), tuned_parameters, cv=10)
    model.fit(X_train, y_train)

    print("Optimised parameters found on training set:")
    print(model.best_estimator_, "\n")

    svc = model.best_estimator_
    svc.fit(X_train, y_train)
    svc.fit(X, y)

    print(svc.score(X_test, y_test))

    df_test = ts.get_hist_data('600179', start='2018-04-01', end='2018-04-25')
    df_test['direction'] =  np.where(df_test['price_change'] > 0, 1, 0)
    df_test = df_test.dropna()
    #df_test.to_csv('1.csv')

    X_test = df_test[["close","low","high","ma5","ma10", "ma20","v_ma5","v_ma10", "v_ma20", "turnover"]]
    y_test = df_test[["direction"]].values.ravel()

    X_test = preprocessing.scale(X_test)

    print(svc.score(X_test, y_test))

    df_test = ts.get_hist_data('600179', start='2018-04-26', end='2018-04-26')
    X_test = df_test[["close","low","high","ma5","ma10", "ma20","v_ma5","v_ma10", "v_ma20", "turnover"]]
    y_test_pred = svc.predict(X_test)
    print(y_test_pred)