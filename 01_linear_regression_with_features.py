# Close price predict

import tushare as ts
from sqlalchemy import create_engine
import custom_feature_calculating.BBANDS as featureLibBB
import custom_feature_calculating.CCI as featureLibCCI
import custom_feature_calculating.FI as featureLibFI
import custom_feature_calculating.EMV as featureLibEVM
import custom_feature_calculating.EWMA as featureLibEWMA
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model

# data collecting
# or extract from db
tick_code = '600179'
df = ts.get_hist_data(tick_code)  # 一次性获取上证数据
df = df.sort_index()

n = 5
# add feature to df
df = featureLibBB.BBANDS(df, n)
df = featureLibCCI.CCI(df, n)
df = featureLibFI.ForceIndex(df, n)
df = featureLibEVM.EVM(df, n)
df = featureLibEWMA.EWMA(df, n)
df = df.dropna()

# print test
print(df.tail(1))

feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi']
# ^^^^^^^ need more features

count = len(df.index)
# traning
train_count = int(len(df.index) * 0.7)
# testing
test_count = int(len(df.index) * 0.3)

# cross validation miss
# !!!!!!!!!!!!!!!!!!


### !!!!!IMPROVEMENT

# get x traning custome features head n rows
df_x_train = df[feature].head(train_count).values

# get traning close price head n rows
df_y_train = df['close'].head(train_count).values

# get x testing custome feature tail n rows
df_x_test = df[feature].tail(test_count).values

# get y tesing custome close price n rows
df_y_test = df['close'].tail(test_count).values

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

df_now = ts.get_realtime_quotes(tick_code)
df_now['ma5'] = df['ma5'].tail(1).values
df_now['ma10'] = df['ma10'].tail(1).values
df_now['ma20'] = df['ma20'].tail(1).values
df_now['ubb'] = df['ubb'].tail(1).values
df_now['lbb'] = df['lbb'].tail(1).values
df_now['cci'] = df['cci'].tail(1).values
df_now['evm'] = df['evm'].tail(1).values
df_now['ewma'] = df['ewma'].tail(1).values
df_now['fi'] = df['fi'].tail(1).values

df_x_toady = df_now[feature].values
print('开盘价格:%s' % df_now[['open']].values)
df_y_toady_pred = reg.predict(df_x_toady);
print('预测价格:%s' % df_y_toady_pred)

# Plot outputs
plt.scatter(df_x_test[:, 0], df_y_test, color='black')
plt.plot(df_x_test[:, 0], df_y_test_pred, color='blue', linewidth=3)
plt.show()
