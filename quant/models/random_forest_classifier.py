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
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation, metrics


class RandomForestClassifierModel(BaseModel):

    def training_model(self, code):
        data = k_data_dao.get_k_data(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        data, features = collect_features(data)

        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        rfc_model = RandomForestClassifier()

        tuned_parameter = [{'n_estimators': range(100, 1000, 100), 'max_depth': range(3, 14, 2), 'min_samples_split': range(50, 200, 10), 'min_samples_leaf': range(10, 60, 10), 'max_features': range(3, 81, 2), 'oob_score': True}]

        g_search = GridSearchCV(estimator=rfc_model, param_grid=tuned_parameter, cv=None, n_jobs=-1)

        search_result = g_search.fit(X_train, y_train)

        print(g_search.grid_scores_, g_search.best_params_, g_search.best_score_)

        print(search_result)




