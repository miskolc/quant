import tushare as ts
from sqlalchemy import create_engine
import feature_lib.BBANDS as featureLibBB
import feature_lib.CCI as featureLibCCI
import feature_lib.FI as featureLibFI
import feature_lib.EVM as featureLibEVM
import feature_lib.EWMA as featureLibEWMA
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn import linear_model

tick_code = '002266'
df = ts.get_hist_data(tick_code, start='2016-01-01', end='2018-04-18') #一次性获取上证数据
df = df.sort_index()

n = 5
#计算Bollinger Bands列
df = featureLibBB.BBANDS(df,n)
df = featureLibCCI.CCI(df,n)
df = featureLibFI.ForceIndex(df,n)
df = featureLibEVM.EVM(df,n)
df = featureLibEWMA.EWMA(df,n)
df = df.dropna()
print(df.tail(1))

feature = ['open', 'ma5','ma10','ma20', 'ubb','lbb','cci','evm', 'ewma','fi']
count = len(df.index)
train_count = int(len(df.index) * 0.7)
test_count = int(len(df.index) * 0.3)

df_x_train = df[feature].head(train_count).values
df_y_train = df['close'].head(train_count).values

df_x_test = df[feature].tail(test_count).values
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

df_x_toady =  df_now[feature].values
print('开盘价格:%s' % df_now[['open']].values)
df_y_toady_pred = reg.predict(df_x_toady);
print('预测价格:%s'% df_y_toady_pred)


# Plot outputs
plt.scatter(df_x_test[:,0], df_y_test,  color='black')
plt.plot(df_x_test[:,0], df_y_test_pred, color='blue', linewidth=3)
plt.show()