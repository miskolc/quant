from sklearn import linear_model
import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')

googDf_All = pd.read_sql_query('SELECT price_date,open_price,close_price FROM daily_price where symbol_id = %s' % (28), engine)

googDf_train = pd.read_sql_query('SELECT price_date,open_price,close_price FROM daily_price where symbol_id = %s and price_date between \'%s\' and  \'%s\'' % (28, '2017-01-01', '2018-01-01'), engine)
googDf_test = pd.read_sql_query('SELECT price_date,open_price,close_price FROM daily_price where symbol_id = %s and price_date >= \'%s\'' % (28, '2018-01-02'), engine)


googDf_x_train = googDf_train['open_price'].values.reshape(len(googDf_train.index), 1)
googDf_y_train = googDf_train['close_price'].values.reshape(len(googDf_train.index), 1)


googDf_x_test = googDf_test['open_price'].values.reshape(len(googDf_test.index), 1)
googDf_y_test = googDf_test['close_price'].values.reshape(len(googDf_test.index), 1)

reg = linear_model.LinearRegression()
reg.fit(googDf_x_train, googDf_y_train)

googDf_y_test_pred = reg.predict(googDf_x_test)

# The coefficients
print('Coefficients: \n', reg.coef_)
# The coefficients
print('Intercept: \n', reg.intercept_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(googDf_y_test, googDf_y_test_pred))

print('Variance score: %.2f' % r2_score(googDf_y_test, googDf_y_test_pred))

googDf_x_all = googDf_All['open_price'].values.reshape(len(googDf_All.index), 1)
googDf_y_all = googDf_All['close_price'].values.reshape(len(googDf_All.index), 1)

reg.fit(googDf_x_all,googDf_y_all)

googDf_x_toady = [[1051.37]]
googDf_y_toady_pred = reg.predict(googDf_x_toady)
print(googDf_y_toady_pred)

# Plot outputs
plt.scatter(googDf_x_test, googDf_y_test,  color='black')
plt.plot(googDf_x_test, googDf_y_test_pred, color='blue', linewidth=3)

#plt.xticks(())
#plt.yticks(())
plt.show()


	