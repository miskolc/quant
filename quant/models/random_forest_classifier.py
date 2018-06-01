# coding = utf-8
# ae_h - 2018/5/30
from datetime import datetime

from quant.models.base_model import BaseModel
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from quant.dao.k_data_dao import k_data_dao
from quant.feature_utils.feature_collector import collect_features
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import cross_validation, metrics


class RandomForestClassifierModel(BaseModel):

    def training_model(self, code, data, features):
        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        rfc_model = RandomForestClassifier(max_features='sqrt', max_depth=14, oob_score=True, n_jobs=-1)

        tuned_parameter = {'n_estimators': [50, ], 'min_samples_leaf': range(10, 60, 10),
                           'min_samples_split': range(20, 100, 20)}

        gs_result = GridSearchCV(estimator=rfc_model, param_grid=tuned_parameter, scoring='roc_auc', cv=None, n_jobs=-1)

        # # 0.557
        # gs_result = RandomForestClassifier(n_estimators=50, max_depth=3, min_samples_split=80,
        #                                    min_samples_leaf=50, max_features=3, oob_score=True, random_state=10)

        gs_result.fit(X_train, y_train)

        print('auc: %s' % gs_result.score(X_test, y_test))

        rf1 = RandomForestClassifier(n_estimators=50, min_samples_leaf=gs_result.best_params_['min_samples_leaf'], min_samples_split=gs_result.best_params_['min_samples_split'], max_features='sqrt', max_depth=3, oob_score=True, n_jobs=-1, random_state=10)

        rf1.fit(X_train, y_train)

        print('oob: %s' % rf1.oob_score_)

