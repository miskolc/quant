# Close price predict

from sklearn import linear_model
from sklearn.model_selection import cross_val_predict, cross_val_score

import app.common_tools.drawer as drawer
import app.common_tools.logger as logger
from app.contants.feature_constant import feature
from app.dao.price_service import get_k_data, get_training_data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# predict
def trained_linear_model(df=None):
    if df is None:
        df = get_training_data('600179', ktype='D', start='2017-01-01', end='2017-10-10')
        # print(df)
    # df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)

    model = linear_model.LinearRegression(normalize=True)

    print('current: %s' % df['next_open'].tail(1).values)
    X = df[feature]
    y = df['next_open']
    predicted = cross_val_predict(model, X, y, cv=10)

    # print(type(y.values))
    # print(type(predicted))

    # print((y.values - predicted))

    model.fit(X, y)
    print((cross_val_score(model, X, y, cv=10).mean()))
    return model


if __name__ == "__main__":
    df_now = get_training_data('600179', ktype='D', start='2018-01-01', end='2018-04-20')
    predict_y = trained_linear_model().predict(df_now[feature].tail(1))
    print(predict_y)