# Close price predict

import tushare as ts
import custom_feature_calculating.BBANDS as featureLibBB
import custom_feature_calculating.CCI as featureLibCCI
import custom_feature_calculating.FI as featureLibFI
import custom_feature_calculating.EMV as featureLibEVM
import custom_feature_calculating.EWMA as featureLibEWMA
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split


def predict(code='600179', show_plot=False):
    df = ts.get_hist_data(code)  # 一次性获取上证数据
    df = df.sort_index()

    # 获取上证指数
    df_sh = ts.get_hist_data('sh')  # 一次性获取上证数据
    n = 5
    # add feature to df
    df = featureLibBB.BBANDS(df, n)
    df = featureLibCCI.CCI(df, n)
    df = featureLibFI.ForceIndex(df, n)
    df = featureLibEVM.EMV(df, n)
    df = featureLibEWMA.EWMA(df, n)
    # 填充上证指数到训练集
    df['rt_sh'] = df_sh['close']
    df = df.dropna()
    # Normalization
    df_norm = (df - df.mean()) / (df.max() - df.min())
    # print test
    # print(df.tail(1))

    feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi']

    # ^^^^^^^ need more features

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['close'], test_size=.3)

    # choose linear regression model
    reg = linear_model.LinearRegression(normalize=True)

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
    df_now['open'] = df_now['close']

    df_x_toady = df_now[feature].values

    print('昨日收盘价格:%s' % df_now[['open']].values)
    df_y_toady_pred = reg.predict(df_x_toady);
    print('预测收盘价格:%s' % df_y_toady_pred)

    # Plot outputs

    if show_plot:
        plt.scatter(df_x_test['open'], df_y_test, color='black')
        plt.plot(df_x_test['open'], df_y_test_pred, color='blue', linewidth=3)
        plt.show()


if __name__ == "__main__":
      code = input("Enter the code: ")
      # code is null
      if not code.strip():
            predict()
      else:
            predict(code)
