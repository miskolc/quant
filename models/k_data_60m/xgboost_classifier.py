# coding = utf-8
# ae_h - 2018/6/1

import os

import xgboost as xgb
from common_tools.decorators import exc_time
from dao.k_data_60m.k_data_60m_model_log_dao import k_data_60m_model_log_dao
from log.quant_logging import logger
from models.base_model import BaseModel
from models.k_data_60m import MODULE_NAME
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

from models.pca_model import PCAModel


class XGBoostClassier(BaseModel):
    module_name = MODULE_NAME
    model_name = "xgb_classifier"

    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3,
                                                            shuffle=False)

        parameters_grid = [{'learning_rate': [0.05, 0.1, 0.3], 'max_depth': range(2, 8, 2), 'subsample': [0.7, ], 'min_child_weight': range(1, 6, 2)}]

        gs_search = GridSearchCV(estimator=xgb.XGBClassifier(n_estimators=100, random_state=10), param_grid=parameters_grid, n_jobs=-1)

        gs_result = gs_search.fit(X_train, y_train)

        logger.debug(gs_search.best_params_)
        logger.debug("XGBoost Classier's best score: %.4f" % gs_result.best_score_)  # 训练的评分结果

        xgb_classifier = gs_search.best_estimator_
        # 使用训练数据, 重新训练
        xgb_classifier.fit(X_train, y_train)

        # 使用测试数据对模型进评平分
        y_test_pred = xgb_classifier.predict(X_test)

        # 在测试集中的评分
        test_score = accuracy_score(y_test, y_test_pred)
        logger.debug('test score: %.4f' % test_score)

        # 使用所有数据, 重新训练
        xgb_classifier.fit(X, y)

        # 记录日志
        k_data_60m_model_log_dao.insert(code=code, name=self.model_name
                                    , best_estimator=gs_search.best_estimator_,
                                    train_score=gs_search.best_score_, test_score=test_score)
        # 输出模型
        joblib.dump(xgb_classifier, self.get_model_path(code, self.module_name, self.model_name))

    @exc_time
    def predict(self, code, data):
        model_path = self.get_model_path(code, self.module_name, self.model_name)

        if not os.path.exists(model_path):
            logger.error('model not found, code is %s:' % code)
            return

        X = preprocessing.scale(data)
        pac = PCAModel(self.module_name).load(code)
        X = pac.transform(X)

        xgb_classifier = joblib.load(model_path)

        y_pred = xgb_classifier.predict(X)

        return int(y_pred[0])



# xgb_search = GridSearchCV(xgb_model, parameters, scoring='roc_auc')
# xgb_search.fit(X, y)
