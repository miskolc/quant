# coding=utf-8
import tushare as ts
from sklearn import preprocessing

import app.custom_feature_calculating.K_w_R_rate as w_R_rate
from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.K_uos import uos
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.MACD as macd
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC, SVC
from xgboost import XGBClassifier
import warnings
import app.test_pack.backup.rf.hs300s.classifier_dao as dao

def predict(code):
    X_pred = dao.predict_data(code)
    X, y = dao.prepare_data(code, ktype='D')

    lg = LogisticRegression()
    lg_scores = cross_val_score(lg, X, y, cv=10)
    # 弱网格测试
    param_test_weak = {'n_estimators': range(900, 1000, 100)}
    gsearch_weak = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,
                                                                 min_samples_leaf=20, max_depth=8, max_features='sqrt',
                                                                 random_state=None),
                                param_grid=param_test_weak, scoring='roc_auc', cv=5)
    gsearch_weak.fit(X, y)

    # SVC
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
    ]
    # Perform the grid search on the tuned parameters
    gsearch_svc = GridSearchCV(SVC(C=1), tuned_parameters, cv=10, n_jobs=-1)
    gsearch_svc.fit(X, y)

    # LinearSVC
    lsvc = LinearSVC(C=1)
    lsvc_scores = cross_val_score(lsvc, X, y, cv=10)

    #XGBClassifier
    xgb_model = XGBClassifier(n_estimators=300)
    parameters = {'learning_rate': [0.01, 0.02, 0.03], 'max_depth': [4, 5, 6]}
    xgb_search = GridSearchCV(xgb_model, parameters, scoring='roc_auc')
    xgb_search.fit(X, y)



    models = [("LR", lg, lg_scores.mean()),
              ("RF", gsearch_weak.best_estimator_, gsearch_weak.best_score_),
              ("SVC", gsearch_svc.best_estimator_, gsearch_svc.best_score_),
              ("LSVC", lsvc, lsvc_scores.mean()),
              ("XGB", xgb_search.best_estimator_, xgb_search.best_score_)
              ]

    pred_list = []
    # with open('/Users/yw.h/Documents/hs300-selection-result.log', 'a', encoding='utf8') as f:
    for m in models:
        m[1].fit(X, y)
        y_test_pred = m[1].predict(X_pred[-1:])
        print("模型:%s, score:%s, 趋势:%s" % (m[0], m[2], y_test_pred))
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
