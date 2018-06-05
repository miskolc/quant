# coding = utf-8
# ae_h - 2018/5/30

import os

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from quant.common_tools.decorators import exc_time
from quant.dao.k_data.k_data_model_log_dao import k_data_model_log_dao
from quant.log.quant_logging import logger
from quant.models.base_model import BaseModel
from quant.models.pca_model import PCAModel
from quant.models.k_data_60m import MODULE_NAME

class RandomForestClassifierModel(BaseModel):
    module_name = MODULE_NAME
    model_name = "random_forest_classifier_model"


    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        rfc_model = RandomForestClassifier(max_features='sqrt', max_depth=14, oob_score=True)

        tuned_parameter = {'n_estimators': [50, ], 'min_samples_leaf': range(10, 60, 10),
                           'min_samples_split': range(20, 100, 20)}

        gs_result = GridSearchCV(estimator=rfc_model, param_grid=tuned_parameter, scoring='roc_auc', cv=None, n_jobs=-1)

        gs_result.fit(X_train, y_train)

        logger.debug('auc: %s' % gs_result.best_score_)

        min_samples_leaf = gs_result.best_params_['min_samples_leaf']
        min_samples_split = gs_result.best_params_['min_samples_split']

        rf1 = RandomForestClassifier(n_estimators=50, min_samples_leaf=min_samples_leaf,
                                     min_samples_split=min_samples_split, max_features='sqrt',
                                     max_depth=3, oob_score=True, n_jobs=-1, random_state=10)

        rf1.fit(X_train, y_train)

        logger.debug('oob: %s' % rf1.oob_score_)

        # 在测试集中的评分
        test_score = rf1.score(X_test, y_test)
        logger.debug('test score: %.4f' % test_score)

        # 使用所有数据, 重新训练
        rf1.fit(X, y)

        rf1_str = "RandomForestClassifier(n_estimators=50, min_samples_leaf=%s" \
                  ",min_samples_split=%s, max_features='sqrt',max_depth=3, " \
                  "oob_score=True, n_jobs=-1, random_state=10)" % (min_samples_leaf, min_samples_split)

        # 记录日志
        k_data_model_log_dao.insert(code=code, name=self.model_name
                                    , best_estimator=rf1_str,
                                    train_score=gs_result.best_score_, test_score=test_score
                                    , desc="oob_score_:%s" % rf1.oob_score_)

        # 输出模型
        joblib.dump(rf1, self.get_model_path(code, self.module_name,self.model_name))

    @exc_time
    def predict(self, code, data):
        model_path = self.get_model_path(code, self.module_name,self.model_name)

        if not os.path.exists(model_path):
            logger.error('model not found, code is %s:' % code)
            return

        X = preprocessing.scale(data)
        pac = PCAModel(self.module_name).load(code)
        X = pac.transform(X)

        rf1 = joblib.load(model_path)

        y_pred = rf1.predict(X)

        return int(y_pred[0])
