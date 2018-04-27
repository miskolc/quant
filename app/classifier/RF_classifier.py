# ae.h - 2018/4/27

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation, metrics
from app.dao.price_service import get_k_data, get_training_data
import tushare as ts


def RF_clf():
    df = ts.bar('600179', conn=ts.get_apis())
    df['price_change'] = df['close'] - df['close'].shift(-1)
    df['direction'] = np.where(df['price_change'] > 0, 1, 0)
    df['direction'] = df['direction'].shift(-1)

    df = df.dropna()
    x = df[["close", "low", "high", "open", "vol", "amount"]]
    y = df['direction'].values.ravel()
    rf0 = RandomForestClassifier(oob_score=True, random_state=10)

    print(x.shape)
    print(y.shape)

    rf0.fit(x, y)
    print(rf0.oob_score_)
    y_predprob = rf0.predict_proba(x)[:, 1]
    print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))
    print('==================================================')

    # 弱网格测试
    param_test_weak = {'n_estimators': range(10, 71, 10)}
    gsearch_weak = GridSearchCV(estimator=RandomForestClassifier(min_samples_split=100,
                                                                 min_samples_leaf=20, max_depth=8, max_features='sqrt',
                                                                 random_state=10),
                                param_grid=param_test_weak, scoring='roc_auc', cv=5)
    gsearch_weak.fit(x, y)
    print('cv_result: %s' % gsearch_weak.cv_results_)

    print(gsearch_weak.grid_scores_, '\n')
    print(gsearch_weak.best_params_, '\n')
    print(gsearch_weak.best_score_)

    强网格测试
    param_test_strong = {'max_depth': range(3, 14, 2), 'min_samples_split': range(50, 201, 20)}
    gsearch_strong = GridSearchCV(estimator=RandomForestClassifier(n_estimators=20,
                                                                   min_samples_leaf=20, max_features='sqrt',
                                                                   oob_score=True,
                                                                   random_state=10),
                                  param_grid=param_test_strong, scoring='roc_auc', iid=False, cv=5)
    gsearch_strong.fit(x, y)
    print(gsearch_strong.grid_scores_, '\n')
    print(gsearch_strong.best_params_, '\n')
    print(gsearch_strong.best_score_)

    rf1 = RandomForestClassifier(n_estimators=20, max_depth=3, min_samples_split=130, oob_score=True, random_state=10)
    rf1.fit(x, y)
    print(rf1.oob_score_)
    y_predprob = rf1.predict_proba(x)[:, 1]
    print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))
    print('==================================================')

    最小样本测试
    param_test_min = {'min_samples_split': range(80, 130, 20), 'min_samples_leaf': range(10, 60, 10)}
    gsearch_min = GridSearchCV(estimator=RandomForestClassifier(n_estimators=20, max_depth=3,
                                                                max_features='sqrt', oob_score=True, random_state=10),
                               param_grid=param_test_min, scoring='roc_auc', iid=False, cv=5)
    gsearch_min.fit(x, y)
    print(gsearch_min.cv_results_, '\n')
    print(gsearch_min.best_params_, '\n')
    print(gsearch_min.best_score_)

    rf2 = RandomForestClassifier(n_estimators=20, max_depth=3, min_samples_split=80, oob_score=True, random_state=10,
                                 min_samples_leaf=50)
    rf2.fit(x, y)
    print(rf2.oob_score_)
    y_predprob = rf2.predict_proba(x)[:, 1]
    print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))
    print('==================================================')

    最大特征测试

    param_test_max = {'max_features': range(3, 6, 2)}
    gsearch_max = GridSearchCV(estimator=RandomForestClassifier(n_estimators=20, max_depth=3, min_samples_split=80,
                                                                min_samples_leaf=50, oob_score=True, random_state=10),
                               param_grid=param_test_max, scoring='roc_auc', iid=False, cv=5)
    gsearch_max.fit(x, y)
    print(gsearch_max.cv_results_, '\n')
    print(gsearch_max.best_params_, '\n')
    print(gsearch_max.best_score_)

    rf3 = RandomForestClassifier(n_estimators=20, max_depth=3, min_samples_split=80,
                                 min_samples_leaf=50, max_features=3, oob_score=True, random_state=10)
    rf3.fit(x, y)
    print(rf3.oob_score_)
    y_predprob = rf3.predict_proba(x)[:, 1]
    print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))
    print('==================================================')


if __name__ == '__main__':
    RF_clf()
