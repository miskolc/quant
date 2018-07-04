# coding=utf-8
import warnings

import tushare as ts
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier


import app.test_pack.backup.rf.hs300s.classifier_dao as dao


def predict(code):
    X_pred = dao.predict_data(code)
    X, y = dao.prepare_data(code, ktype='D')


    lg = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr',
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)

    #RF
    rf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=3, max_features='sqrt', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=20, min_samples_split=120,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=-1,
            oob_score=True, random_state=10, verbose=0, warm_start=False)

    # SVC
    svc = SVC(C=1, cache_size=200, class_weight=None, coef0=0.0,
      decision_function_shape='ovr', degree=3, gamma=0.001, kernel='rbf',
      max_iter=-1, probability=False, random_state=None, shrinking=True,
      tol=0.001, verbose=False)

    # LinearSVC
    lsvc = LinearSVC(C=1, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0)

    # XGBClassifier
    xgb = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, cv=5, gamma=0, learning_rate=0.03,
       max_delta_step=0, max_depth=4, min_child_weight=1, missing=None,
       n_estimators=100, n_jobs=-1, nthread=None, objective='binary:logistic',
       random_state=0, reg_alpha=0, reg_lambda=1, scale_pos_weight=1,
       seed=None, silent=True, subsample=1)


    models = [("LR", lg),
              ("RF", rf),
              ("SVC", svc),
              ("LSVC", lsvc),
              ("XGB", xgb),
              ]

    #print(xgb_search.best_estimator_.feature_importances_)

    pred_list = []
    # with open('/Users/yw.h/Documents/hs300-selection-result.log', 'a', encoding='utf8') as f:
    for m in models:
        m[1].fit(X, y)

        y_test_pred = m[1].predict(X_pred[-1:])

        print("模型:%s, 趋势:%s" % (m[0], y_test_pred))
        # f.writelines("股票代码: %s 模型:%s, score:%s, 趋势:%s \n" % (code, m[0], m[2], y_test_pred))
        pred_list.append(y_test_pred[0])
        if hasattr(m[1], 'feature_importances_'):
            print(m[1].feature_importances_)

    return pred_list


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    code = input("Enter the code: ")
    if not code.strip():
        code = '600179'

    predict(code)
