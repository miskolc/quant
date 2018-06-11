import unittest
from datetime import datetime

from quant.dao.k_data_60m.k_data_60m_dao import k_data_60m_dao

from quant.dao.k_data_60m.index_k_data_60m_dao import index_k_data_60m_dao
from quant.log.quant_logging import logger
from quant.models.k_data_60m.logistic_regression_classifier import LogisticRegressionClassifier
from quant.models.pca_model import PCAModel
from quant.test import before_run
from quant.models.k_data_60m import MODULE_NAME

class Logistic_Regression_Classifier_60m_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_60m_dao.get_k_data_with_features(code, '2015-01-01',
                                                             datetime.now().strftime("%Y-%m-%d"))

        logger.debug("features:%s, length:%s" % (features, len(features)))

        data.to_csv("result.csv")
        pac = PCAModel(MODULE_NAME);
        pac.training_model(code=code, data=data,features=features)

        model = LogisticRegressionClassifier()
        model.training_model(code, data, features)


    def test_predict(self):
        code = '600196'
        df_index = index_k_data_60m_dao.get_rel_price();

        df, features = k_data_60m_dao.get_k_predict_data_with_features("600196", df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = LogisticRegressionClassifier()
        y_predict = model.predict(code, df[features])

        print(y_predict)

