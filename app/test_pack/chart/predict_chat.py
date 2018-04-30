# Close price predict

from sklearn import linear_model
from sklearn.model_selection import train_test_split

import app.common_tools.drawer as drawer
import app.common_tools.logger as logger
from app.contants.feature_constant import feature
from app.dao.price_service import get_k_data, get_training_data
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR


def cross_validation(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]

    # Perform the grid search on the tuned parameters
    model = GridSearchCV(SVR(C=1), tuned_parameters, cv=10)
    model.fit(X_train, y_train)

    print("Optimised parameters found on training set:")
    print(model.best_params_, "\n")
    print(model.best_estimator_, "\n")

    return model.best_estimator_


# predict
def predict(code='601398', show_plot=False, df=None, df_now=None):
    if df is None:
        df = get_training_data(code, 'D', start='2018-01-01', end='2018-04-30')

    # df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)

    X = df[feature]
    index = [x[5:] for x in X.index.values]
    X = preprocessing.scale(df[feature])
    y = df['next_open']
    # lasso
    lasso = linear_model.LassoCV(alphas=[10, 1, 0.5, 0.25, 0.1, 0.005, 0.0025, 0.001])
    lasso.fit(X, y)

    # Ridge
    ridge = linear_model.RidgeCV(alphas=[0.01, 0.01, 0.1, 1.0, 10.0], normalize=True)
    ridge.fit(X, y)

    # SVR
    best_estimator_ = cross_validation(X, y)
    svr = best_estimator_
    svr.fit(X, y)

    y_lasso_pred = lasso.predict(X)
    y_svr_pred = svr.predict(X)
    y_ridge_pred = ridge.predict(X)

    fig, ax = plt.subplots(figsize=(16, 10))

    ax.scatter(index, y, color='red', label='Price')
    ax.plot(index, y_lasso_pred,  label='Lasso')
    ax.plot(index, y_ridge_pred,  label='Ridge')
    ax.plot(index, y_svr_pred,  label='SVR')
    ax.grid(True)

    plt.xticks(rotation=60)
    plt.xlabel('Day/Month')
    plt.ylabel('Price')
    plt.title('%s Daily Prices' % (code))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict(show_plot=True)
    else:
        predict(code)
