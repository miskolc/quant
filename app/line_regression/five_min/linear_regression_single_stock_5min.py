# Close price predict

import matplotlib.pyplot as plt
import tushare as ts
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from app.custom_feature_calculating import feature as feature_service
from app.dao.price_service import get_open_price
from sklearn import linear_model
from app.line_regression.five_min.feature_constant import feature


# predict
def predict(code='600179', show_plot=False):
    df = ts.get_hist_data(code, ktype='5')
    df = df.sort_index()
    df['next_open'] = df['open'].shift(-1)

    # add feature to df
    df = feature_service.fill_for_line_regression_5min(df)
    df = df.dropna()

    # ^^^^^^^ need more features

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)

    # choose linear regression model
    reg = linear_model.LinearRegression()

    # fit model with data(training)
    reg.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = reg.predict(df_x_test)

    # The Coefficients (系数 auto gen)
    print('Coefficients: \n', reg.coef_)
    # The Intercept(截距/干扰/噪声 auto gen)
    print('Intercept: \n', reg.intercept_)
    # The mean squared error(均方误差)
    print("Mean squared error: %.2f"
          % mean_squared_error(df_y_test, df_y_test_pred))

    # r2_score - sklearn评分方法
    print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))

    reg.fit(df[feature], df['next_open'])

    df_now = ts.get_hist_data(code, ktype='5')
    df_now = df_now.sort_index()
    df_now = feature_service.fill_for_line_regression_5min(df_now)

    print('当前价格:%s' % df_now['close'].tail(1).values)
    df_y_toady_pred = reg.predict(df_now[feature].tail(1));
    print('Linear Regression Model, 预测价格:%s' % df_y_toady_pred)

    # Plot outputs

    if show_plot:
        plt.scatter(df_x_test.index, df_y_test, color='black')
        plt.scatter(df_x_test.index, df_y_test_pred, color='blue')
        plt.show()

    return df_y_toady_pred


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():

        predict()
    else:
        predict(code)
