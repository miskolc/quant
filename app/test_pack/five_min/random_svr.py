# ae.h - 2018/4/27
# Close price predict

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sqlalchemy import create_engine

import app.common_tools.logger as logger
import app.custom_feature_calculating.feature as feature_service
from app.contants.feature_constant import feature
from quant.dao import get_k_data


def cross_validation(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]
    # Perform the grid search on the tuned parameters
    model = GridSearchCV(SVR(C=1), tuned_parameters, cv=10, n_jobs=-1)
    model.fit(X_train, y_train)

    print("best estimator found on training set:")
    print(model.best_estimator_, "\n")

    return model.best_estimator_


# predict
def predict(code='600179', ktype='5', show_plot=False, df=None, df_now=None):
    if df is None:
        sql = 'SELECT  t1.datetime,t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.open as sh_open, t2.close as sh_close' \
              ' from tick_data_5min t1' \
              ' LEFT JOIN tick_data_5min t2 on t1.datetime = t2.datetime and t2.code=\'sh\'' \
              ' where t1.code in (\'%s\')' % code
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')
        df = pd.read_sql_query(sql, engine, index_col='datetime')

        df['next_open'] = df['open'].shift(-1)

        # add feature to df
        df = feature_service.fill_db_5min(df, ktype)
        print(df)
        df = df.dropna()
    X = preprocessing.scale(df[feature])
    y = df['next_open']
    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(X, y, test_size=.3, random_state=21)
    best_estimator_ = cross_validation(X, y)
    # choose SVR model
    svr = best_estimator_
    # fit model with data(training)
    svr.fit(df_x_train, df_y_train)
    # test predict
    df_y_test_pred = svr.predict(df_x_test)
    logger.log_model(svr, df_y_test, df_y_test_pred)

    svr.fit(X, y)

    if df_now is None:
        df_now = get_k_data(code, ktype)

    df_x_now = df_now[feature].tail(1)
    print('当前价格:%s' % df_x_now['close'].values)
    df_y_toady_pred = svr.predict(preprocessing.scale(df_x_now));

    print('SVR Model, 预测价格:%s' % df_y_toady_pred)

    if show_plot:
        plt.scatter(df_x_test[:, 0], df_y_test, color='black')
        plt.scatter(df_x_test[:, 0], df_y_test_pred, color='blue')
        plt.show()

    return df_y_toady_pred, df_x_now['close'].values[0]


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict(show_plot=False)
    else:
        predict(code)
