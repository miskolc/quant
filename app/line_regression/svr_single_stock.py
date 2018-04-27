# Close price predict

import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

import app.common_tools.logger as logger
from app.contants.feature_constant import feature
from app.dao.price_service import get_k_data, get_training_data


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
    '''
    #The grid_scores_ attribute was deprecated in version 0.18
    
    
    print("Grid scores calculated on training set:")
    for params, mean_score, scores in model.grid_scores_:
         print("%0.3f for %r" % (mean_score, params))
    
    print("Grid scores calculated on training set:")
    means = model.cv_results_['mean_test_score']
    stds = model.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, model.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    '''

    return model.best_params_


# predict
def predict(code='600179', ktype='5', show_plot=False, df = None, df_now=None):
    if df is None:
        df = get_training_data(code, ktype)
    # ^^^^^^^ need more features
    X = preprocessing.scale(df[feature])
    y = df['next_open']
    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(X, y, test_size=.3, random_state=21)

    best_params_ = cross_validation(X, y)

    # choose SVR model
    svr = SVR(kernel=str('rbf'), C=best_params_['C'], gamma=best_params_['gamma'],
              cache_size=200, degree=3, epsilon=1, max_iter=-1, shrinking=True, tol=0.001, verbose=False)

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
