# Close price predict

import matplotlib.pyplot as plt
import tushare as ts
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from app.custom_feature_calculating import feature as feature_service
from dao import get_open_price


# predict
def predict(code='600179', show_plot=False):
    df = ts.get_hist_data(code, start='2015-01-01')  # 一次性获取上证数据
    df = df.sort_index()

    # add feature to df
    df = feature_service.fill_for_line_regression_predict(df)
    df = df.dropna()

    feature = ['open', 'low', 'high','price_change', 'volume'
                ,'ma_price_change_5','ma_price_change_10','ma_price_change_20'
                ,'v_ma5','v_ma10','v_ma20'
                ,'ma5', 'ma10', 'ma20'
                ,'ubb', 'lbb', 'cci', 'evm'
                , 'ewma', 'fi', 'turnover', 'pre_close'
                , 'sh_open', 'sh_close','macd']
    # ^^^^^^^ need more features

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['close'], test_size=.3)

    # choose linear regression model
    reg = LassoCV(alphas=[1, 0.5, 0.25, 0.1, 0.005, 0.0025, 0.001], normalize=True)

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

    reg.fit(df[feature], df['close'])

    df_now = df.tail(1)
    df_now = df_now.dropna()
    df_now['open'] = get_open_price(code)

    print('今日开盘价格:%s' % df_now[['open']].values)
    df_y_toady_pred = reg.predict(df_now[feature]);
    print('预测收盘价格:%s' % df_y_toady_pred)

    # Plot outputs

    if show_plot:
        plt.scatter(df_x_test.index, df_y_test, color='black')
        plt.scatter(df_x_test.index, df_y_test_pred, color='blue')
        plt.show()


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict()
    else:
        predict(code)
