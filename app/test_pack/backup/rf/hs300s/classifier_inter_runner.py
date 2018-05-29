# coding=utf-8
import warnings

import tushare as ts
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier
import app.test_pack.backup.rf.hs300s.classifier_dao as dao
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def predict(code):
    X_pred = dao.predict_data(code)
    X, y = dao.prepare_data(code, ktype='D')

    pca = PCA(n_components=10)
    pca.fit(X)
    X = pca.transform(X)
    X_pred = pca.transform(X_pred)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                        shuffle=False)



    lg = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr',
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)

    #RF
    rf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=3, max_features='sqrt', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=20, min_samples_split=120,
            min_weight_fraction_leaf=0.0, n_estimators=1000, n_jobs=-1,
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

    lg.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    svc.fit(X_train, y_train)
    lsvc.fit(X_train, y_train)
    xgb.fit(X_train, y_train)


    lg_y_predict = lg.predict(X_train)
    rf_y_predict = rf.predict(X_train)
    svc_y_predict = svc.predict(X_train)
    lsvc_y_predict = lsvc.predict(X_train)
    xgb_y_predict = xgb.predict(X_train)

    data = {
        "lg": lg_y_predict,
        "rf": rf_y_predict,
        "svc": svc_y_predict,
        "lsvc": lsvc_y_predict,
        "xgb": xgb_y_predict,
    }

    X_train = pd.DataFrame(data)
    #X.to_csv('result.csv')

    ilg = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=1, cv=5, gamma=0, learning_rate=0.03,
       max_delta_step=0, max_depth=4, min_child_weight=1, missing=None,
       n_estimators=1000, n_jobs=-1, nthread=None, objective='binary:logistic',
       random_state=0, reg_alpha=0, reg_lambda=1, scale_pos_weight=1,
       seed=None, silent=True, subsample=1)
    ilg.fit(X_train, y_train)

    print(ilg.score(X_train, y_train))



    lg_y_test = lg.predict(X_test)
    rf_y_test = rf.predict(X_test)
    svc_y_test= svc.predict(X_test)
    print("scv test score:",svc.score(X_test, y_test))
    lsvc_y_test = lsvc.predict(X_test)
    xgb_y_test = xgb.predict(X_test)
    data = {
        "lg": lg_y_test,
        "rf": rf_y_test,
        "svc": svc_y_test,
        "lsvc": lsvc_y_test,
        "xgb": xgb_y_test,
    }
    X_test = pd.DataFrame(data)
    y_test_pred = ilg.predict(X_test)


    #score = ilg.score(X_test, y_test_pred)
    print('accuracy score: %.2f' % accuracy_score(y_test, y_test_pred))
    print(ilg.score(X_test, y_test))


    lg.fit(X, y)
    rf.fit(X, y)
    svc.fit(X, y)
    lsvc.fit(X, y)
    xgb.fit(X, y)

    lg_y_all = lg.predict(X)
    rf_y_all = rf.predict(X)
    svc_y_all= svc.predict(X)
    lsvc_y_all = lsvc.predict(X)
    xgb_y_all = xgb.predict(X)
    data = {
        "lg": lg_y_all,
        "rf": rf_y_all,
        "svc": svc_y_all,
        "lsvc": lsvc_y_all,
        "xgb": xgb_y_all,
    }

    X_all = pd.DataFrame(data)
    ilg.fit(X_all, y)
    print(ilg.score(X_all,y))

    #X = pd.DataFrame(data)

    lg_y_pred = lg.predict(X_pred)
    rf_y_pred = rf.predict(X_pred)
    svc_y_pred= svc.predict(X_pred)
    lsvc_y_pred = lsvc.predict(X_pred)
    xgb_y_pred = xgb.predict(X_pred)
    data = {
        "lg": lg_y_pred,
        "rf": rf_y_pred,
        "svc": svc_y_pred,
        "lsvc": lsvc_y_pred,
        "xgb": xgb_y_pred,
    }

    X_pred = pd.DataFrame(data)

    y_pred = ilg.predict(X_pred)

    print(y_pred)

    models = [("LR", lg),
              ("RF", rf),
              ("SVC", svc),
              ("LSVC", lsvc),
              ("XGB", xgb),
              ]





    #print(xgb_search.best_estimator_.feature_importances_)
    '''
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
    '''


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)

    code = input("Enter the code: ")
    if not code.strip():
        code = '600179'

    predict(code)
