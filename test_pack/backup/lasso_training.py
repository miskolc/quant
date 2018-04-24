# lasso model trainng and  predict
import tushare as ts
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split
import pandas as pd
from dao import engine
from sklearn.externals import joblib
from custom_feature_calculating import feature as feature_service
import numpy as np

# predict


feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'evm', 'ewma', 'fi', 'rt_sh']


def train(code='600179', show_plot=True):
    sql = 'SELECT  t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.close as rt_sh' \
          ' from tick_data_1min_hs300 t1' \
          ' LEFT JOIN tick_data_1min_sh t2 on t1.datetime = t2.datetime and t2.code=\'sh\'' \
          ' where t1.code =\'%s\'' % code

    df = pd.read_sql_query(sql, engine.create())
    df = feature_service.fill_for_line_regression(df)

    df = df.dropna()
    df.to_csv("result.csv")
    # print(df[~df.isin([ np.inf, -np.inf]).any(1)])

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

    joblib.dump(reg, 'model/lasso.pkl')
    if show_plot:
        plt.scatter(df_x_test['open'], df_y_test, color='black')
        plt.plot(df_x_test['open'], df_y_test_pred, color='blue', linewidth=3)
        plt.show()


def predict_daily(code):
    reg = joblib.load('model/lasso.pkl');

    df = ts.get_hist_data(code, start='2018-03-01')  # 一次性获取上证数据
    # 获取上证指数
    df_sh = ts.get_hist_data('sh', start='2018-03-01')  # 一次性获取上证数据
    df = df.sort_index()
    # 填充上证指数到训练集
    df['rt_sh'] = df_sh['close']
    df = feature_service.fill_for_line_regression_predict(df)
    df = df.dropna()

    df_today = df.tail(1)
    df_today['open'] = df['close']

    print('昨日收盘价格:%s' % df_today[['open']].values)
    df_x_toady = df[feature].tail(1).values
    df_y_toady_pred = reg.predict(df_x_toady);
    print('预测收盘价格:%s' % df_y_toady_pred)


def predict_min(code):
    reg = joblib.load('model/lasso.pkl');
    conn = ts.get_apis()
    try:
        df = ts.bar(conn=conn, code=code, freq='1min',
                    start_date='2018-04-24', end_date='2018-04-24')

        df = df.rename(columns={'vol': 'volume'})

        df = feature_service.fill_for_line_regression(df)
        df = df.dropna()

        df_sh = ts.bar(conn=conn, code='000001', asset='INDEX', freq='1min',
                       start_date='2018-04-24', end_date='2018-04-24')

        df['rt_sh'] = df_sh['close']

        df_today = df.head(1)
        print(df_today)
        df_today['open'] = df['close']
        print('输入价格:%s' % df_today[['open']].values)
        df_x_toady = df[feature].tail(1).values
        df_y_toady_pred = reg.predict(df_x_toady);
        print('预测价格:%s' % df_y_toady_pred)


    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


if __name__ == "__main__":
    predict_min('600179')
