# coding = utf-8
# ae_h - 2018/6/1


import os

from sklearn import preprocessing
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

from quant.dao.k_data_model_log_dao import k_data_model_log_dao
from quant.log.quant_logging import quant_logging as logging
from quant.models.base_model import BaseModel
from quant.models.pca_model import PCAModel


class SupportVectorRegressionModel(BaseModel):
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放

        pac = PCAModel().load(code)
        X = pac.transform(X)

        # split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                            shuffle=False)

        tuned_parameters = [
            {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]

        # gs
        grid = GridSearchCV(svm.LinearSVR, tuned_parameters, cv=None, n_jobs=-1)
        grid.fit(X_train, y_train)

    def predict(self, code, data, features):
        pass
