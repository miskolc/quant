from sklearn.metrics import mean_squared_error, r2_score


def log_model(reg, df_y_test, df_y_test_pred):

    if hasattr(reg, 'alpha_'):
        print('Alpha: \n', reg.alpha_)

    if hasattr(reg, 'coef_'):
        # The Coefficients (系数 auto gen)
        print('Coefficients: \n', reg.coef_)

    if hasattr(reg, 'intercept_'):
        # The Intercept(截距/干扰/噪声 auto gen)
        print('Intercept: \n', reg.intercept_)

    if hasattr(reg, 'dual_coef_'):

        print('dual_coef_: \n', reg.dual_coef_)

    # The mean squared error(均方误差)
    print("Mean squared error: %.2f"
          % mean_squared_error(df_y_test, df_y_test_pred))
    # r2_score - sklearn评分方法
    print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))