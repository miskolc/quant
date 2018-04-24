# Close price predict

import tushare as ts
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from custom_feature_calculating import feature as feature_service
from sklearn.svm import SVR
import pandas as pd
from sklearn.model_selection import GridSearchCV


def cross_validation(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]

    # Perform the grid search on the tuned parameters
    model = GridSearchCV(SVR(C=1), tuned_parameters, cv=10)
    model.fit(X_train, y_train)

    print("Optimised parameters found on training set:")
    print(model.best_estimator_, "\n")

    print("Grid scores calculated on training set:")
    for params, mean_score, scores in model.grid_scores_:
        print("%0.3f for %r" % (mean_score, params))


# predict
def predict(code='600179', show_plot=False):
    df = ts.get_hist_data(code, start='2015-01-01')  # 一次性获取上证数据
    df = df.sort_index()

    # add feature to df
    df = feature_service.fill_for_line_regression_predict(df)
    df = df.dropna()

    feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi', 'turnover']
    # ^^^^^^^ need more features

    X = df[feature].copy()
    X = preprocessing.scale(X)
    y = df['close']
    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(X, y, test_size=.3, random_state=42)

    cross_validation(X, y)

    # choose SVR model
    svr = SVR(kernel=str('rbf'), C=1000, gamma=0.001)

    # fit model with data(training)
    svr.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = svr.predict(df_x_test)

    # The Coefficients (系数 auto gen)
    # print('Coefficients: \n', svr.coef_)
    # The Intercept(截距/干扰/噪声 auto gen)
    print('Intercept: \n', svr.intercept_)
    # The mean squared error(均方误差)
    print("Mean squared error: %.2f"
          % mean_squared_error(df_y_test, df_y_test_pred))

    # r2_score - sklearn评分方法
    print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))

    svr.fit(df[feature], df['close'])

    df_now = df.tail(1)
    df_now['open'] = df_now['close']

    print('昨日收盘价格:%s' % df_now[['open']].values)
    df_y_toady_pred = svr.predict(preprocessing.scale(df_now[feature]));
    print('预测收盘价格:%s' % df_y_toady_pred)

    # Plot outputs
    #print(df_x_test[:, 0])
    if show_plot:
        plt.scatter(df_x_test[:, 0], df_y_test, color='black')
        plt.scatter(df_x_test[:, 0], df_y_test_pred, color='blue')
        plt.show()


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict(show_plot=True)
    else:
        predict(code)
