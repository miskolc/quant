# Close price predict

from sklearn import linear_model
from sklearn.model_selection import train_test_split

import app.common_tools.drawer as drawer
import app.common_tools.logger as logger
from app.contants.feature_constant import feature
from dao import get_k_data, get_training_data


# predict
def predict(code='600179', ktype='5', show_plot=False, df=None, df_now=None):
    if df is None:
        df = get_training_data(code, ktype)

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)

    # choose ridge regression model
    reg = linear_model.LassoCV(alphas=[10, 1, 0.5, 0.25, 0.1, 0.005, 0.0025, 0.001], normalize=True)

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
