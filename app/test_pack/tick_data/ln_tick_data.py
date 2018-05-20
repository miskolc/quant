import sys

sys.path.append('/Users/chenchenzhong/02-project-test/666-quant-awesome')

from sqlalchemy import create_engine
import pandas as pd
from app.custom_feature_calculating.MACD import fill
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from app.common_tools.logger import log_model
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from quant.dao import price_retrieval_realtime_quotes
from time import sleep
from sklearn.externals import joblib
from datetime import datetime

feature = ['price', 'macd']


def prepare_tick_data_from_db(code):
    sql = 'SELECT id,`date`, price, code from tick_data order by date'

    engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')
    df = pd.read_sql_query(sql, engine, index_col="id")
    df['next_price'] = df['price'].shift(-1)
    df = fill(df, col='price')
    df = df.dropna()
    df.to_csv('result.csv')
    X = df[feature]
    y = df['next_price']

    return X, y


def prepare_rt_data_from_db(code):
    sql = 'select t.id,t.`date`, t.price, t.code from (SELECT id,`date`, price, ' \
          'code from tick_data_rt order by date desc limit 0,100 ) as t where t.code=\'%s\' order by t.`date` ' % code

    engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')
    df = pd.read_sql_query(sql, engine, index_col="id")
    df = fill(df, col='price')
    df = df.dropna()
    X = df[feature]

    return X


def tran(code='600179', show_plot=False):
    X, y = prepare_tick_data_from_db(code)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False)
    model = linear_model.LinearRegression(normalize=True)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    log_model(model, y_test, y_pred)

    joblib.dump(model, 'model.pkl')

    # Plot outputs
    if show_plot is True:
        plt.scatter(x_test["price"], y_test, color='black')
        plt.scatter(x_test["price"], y_pred, color='blue')
        plt.show()


def gmb_test(code='600179'):
    X, y = prepare_tick_data_from_db(code);
    adf_result = list(adfuller(X['macd']))
    print('\n')

    test_statics = adf_result[0]
    p_value = adf_result[1]
    critical_value_1 = adf_result[4]['1%']
    critical_value_5 = adf_result[4]['5%']
    critical_value_10 = adf_result[4]['10%']

    print('test statics: %s' % test_statics)
    print('p_value: %s' % p_value)
    print('critical value 1%%: %s' % critical_value_1)
    print('critical value 5%%: %s' % critical_value_5)
    print('critical value 10%%: %s' % critical_value_10)


def predict(code='600179'):
    model = joblib.load('model.pkl');

    while True:
        sleep(5)
        price_retrieval_realtime_quotes(code)

        X = prepare_rt_data_from_db(code)

        if len(X.index) < 1:
            continue

        y_pred = model.predict(X.tail(1)).round(4);
        dt = datetime.now()
        price = X['price'].tail(1).values[0]

        deviation = y_pred[0] - price

        if deviation >= 0:
            print(
                '%s, 幅度:\033[0;37;41m%.4f ↑\033[0m,当前价格:%s, 预测价格:%s' % (
                    dt.strftime('%Y-%m-%d %H:%M:%S'), deviation, price, y_pred[0]))

        else:
            print(
                '%s, 幅度:\033[0;37;42m%.4f ↓\033[0m,当前价格:%s, 预测价格:%s' % (
                    dt.strftime('%Y-%m-%d %H:%M:%S'), deviation, price, y_pred[0]))


#tran(show_plot=False)

if __name__ == "__main__":
    predict('600179')



# gmb_test()


# df = ts.get_realtime_quotes('600179') #Single stock symbol
# print(df.columns.values)
