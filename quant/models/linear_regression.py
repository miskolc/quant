# ae.h - 2018/5/20

from sklearn import linear_model, metrics
from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
import numpy as np


def trained_linear_model(data=None):
    LR_model = linear_model.LinearRegression(normalize=True, n_jobs=-1)

    X_train, X_test, y_train, y_test = train_test_split(data[feature], data['next_direction'], test_size=.3)

    LR_model.fit(X_train, y_train)

    y_pred = LR_model.predict(X_test)

    y_pred_cv = cross_val_predict(LR_model, X_test, y_test, cv=10)

    print("MSE:", metrics.mean_squared_error(y_test, y_pred))
    print("RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print("MSE after CV:", metrics.mean_squared_error(y_test, y_pred_cv))
    print("RMSE after CV:", np.sqrt(metrics.mean_squared_error(y_test, y_pred_cv)))
    print(cross_val_score(LR_model, X_test, y_test, cv=10).mean())

    return LR_model
