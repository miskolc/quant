# lasso model trainng and  predict

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
def train(code='600179', show_plot=True):

    sql = 'SELECT  t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.close as rt_sh' \
          ' from tick_data_1min_hs300 t1' \
          ' LEFT JOIN tick_data_1min_sh t2 on t1.datetime = t2.datetime and t2.code=\'sh\'' \
          ' where t1.code in (\'000001\' )'

    df = pd.read_sql_query(sql, engine.create())
    df = feature_service.fill_for_line_regression(df)

    df = df.dropna()

    #print(df[~df.isin([ np.inf, -np.inf]).any(1)])

    feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi', 'rt_sh']

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



if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        train()
    else:
        train(code)
