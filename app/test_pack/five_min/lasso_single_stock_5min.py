# Close price predict

from sklearn import linear_model
from sklearn.model_selection import train_test_split

import app.common_tools.drawer as drawer
import app.common_tools.logger as logger
from app.contants.feature_constant import feature
from app.dao.price_service import get_k_data, get_training_data
from sqlalchemy import create_engine
import pandas as pd
import app.custom_feature_calculating.feature as feature_service

# predict
def predict(code='600179', ktype='5', show_plot=False, df=None, df_now=None):
    if df is None:
        sql = 'SELECT  t1.datetime,t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.open as sh_open, t2.close as sh_close' \
              ' from tick_data_5min t1' \
              ' LEFT JOIN tick_data_5min t2 on t1.datetime = t2.datetime and t2.code=\'sh\'' \
              ' where t1.code in (\'%s\')' % code
        engine = create_engine('mysql+pymysql://root:root@localhost:3306/quantitative')
        df = pd.read_sql_query(sql, engine,index_col='datetime')

        df['next_open'] = df['open'].shift(-30)

        # add feature to df
        df = feature_service.fill_db_5min(df)
        df.to_csv('result.csv')
        df = df.dropna()


    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)

    # choose ridge regression model
    reg = linear_model.LassoCV(alphas=[10, 1, 0.5, 0.25, 0.1], normalize=True)

    # fit model with data(training)
    reg.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = reg.predict(df_x_test)

    logger.log_model(reg, df_y_test, df_y_test_pred)

    reg.fit(df[feature], df['next_open'])

    if df_now is None:
        df_now = get_k_data(code, ktype)

    print('当前价格:%s' % df_now['close'].tail(1).values)
    df_y_toady_pred = reg.predict(df_now[feature].tail(1));
    print('Lasso Model, 预测价格:%s' % df_y_toady_pred)

    # Plot outputs
    drawer.make_training_plt(show_plot, df_x_test, df_y_test, df_y_test_pred)

    return df_y_toady_pred


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict()
    else:
        predict(code)
