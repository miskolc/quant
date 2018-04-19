import tushare as ts

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
import time  


#df_sh = ts.get_hist_data('sh',start='2016-01-01',end='2018-04-17', ktype='60') #一次性获取上证数据
df = ts.get_hist_data('600179') #一次性获取上证数据

#df['sh_open'] = df_sh['open']

count = len(df.index)
train_count = int(len(df.index) * 0.7)
test_count = int(len(df.index) * 0.3)


df_x_all = df[['open']].values
df_y_all = df['close'].values

df_x_train = df[['open']].head(train_count).values
df_y_train = df['close'].head(train_count).values

df_x_test = df[['open']].tail(test_count).values
df_y_test = df['close'].tail(test_count).values

reg = linear_model.LinearRegression()
reg.fit(df_x_train, df_y_train)

df_y_test_pred = reg.predict(df_x_test)

# The coefficients
print('Coefficients: \n', reg.coef_)
# The coefficients
print('Intercept: \n', reg.intercept_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(df_y_test, df_y_test_pred))

print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))

reg.fit(df_x_all, df_y_all)
df_y_all_pred = reg.predict(df_x_all)



df_now = ts.get_realtime_quotes("600179")
df_x_toady =  df_now[['price']].values
print('开盘价格:%s' % df_now[['price']].values)
df_y_toady_pred = reg.predict(df_x_toady);
print('预测价格:%s'% df_y_toady_pred)


# Plot outputs
plt.scatter(df_x_all, df_y_all,  color='black')
plt.plot(df_x_all, df_y_all_pred, color='blue', linewidth=3)
plt.show()