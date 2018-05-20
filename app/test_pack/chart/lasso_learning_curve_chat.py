# Close price predict

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.model_selection import learning_curve

from app.contants.feature_constant import feature
from app.dao import get_training_data


# predict
def predict(code='601398', show_plot=False, df=None, df_now=None):
    if df is None:
        df = get_training_data(code, 'D', start='2016-01-01', end='2018-04-30')
    X = df[feature]
    y = df['next_open']

    reg = linear_model.Lasso(alpha=0.1)

    #print(reg.alpha_)

    train_sizes, train_loss, test_loss = learning_curve(
        reg,
        X, y, cv=10, scoring='neg_mean_squared_error',
        train_sizes=[0.1, 0.25, 0.5, 0.75, 1])

    train_loss_mean = -np.mean(train_loss, axis=1)
    test_loss_mean = -np.mean(test_loss, axis=1)

    plt.plot(train_sizes, train_loss_mean, 'o-', color="r",
             label="Training")
    plt.plot(train_sizes, test_loss_mean, 'o-', color="g",
             label="Cross-validation")

    plt.xlabel("Training examples")
    plt.ylabel("Loss")
    plt.legend(loc="best")
    plt.show()

    #df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['next_open'], test_size=.3)
    '''

    # choose ridge regression model
    reg = linear_model.LassoCV(alphas=[10, 1, 0.5, 0.25, 0.1, 0.005, 0.0025, 0.001])

    reg.fit(X, y)

    y_pred = reg.predict(X)

    index = [x[5:] for x in X.index.values]
    fig, ax = plt.subplots(figsize=(16,10))

    ax.scatter(index, y, color='red', label='Price')
    ax.plot(index, y_pred, color='blue', label='Predict Price')

    plt.xticks(rotation=60)
    plt.xlabel('Day/Month')
    plt.ylabel('Price')
    plt.title('%s Daily Prices' % (code))
    plt.legend()
    plt.show()
    '''

if __name__ == "__main__":
    code = input("Enter the code: ")
    # code is null
    if not code.strip():
        predict(show_plot=True)
    else:
        predict(code)
