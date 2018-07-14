import unittest
from datetime import datetime

from dao.k_data_60m.index_k_data_60m_dao import index_k_data_60m_dao
from dao.k_data_60m.k_data_60m_dao import k_data_60m_dao
from log.quant_logging import logger
from models.k_data_60m import MODULE_NAME
from models.k_data_60m.support_vector_classifier import SupportVectorClassifier
from test import before_run

from models.pca_model import PCAModel


class Support_Vector_Classifier_60m_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600276'
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_60m_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logger.debug("features:%s" % features)

        data.to_csv('result.csv')
        pac = PCAModel(MODULE_NAME);
        pac.training_model(code=code, data=data,features=features)

        model = SupportVectorClassifier()
        model.training_model(code, data, features)

    def test_predict(self):
        code='600276'
        df_index = index_k_data_60m_dao.get_rel_price();
        df, features = k_data_60m_dao.get_k_predict_data_with_features("600196", df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = SupportVectorClassifier()
        y_predict = model.predict(code, df[features])

        logger.debug("predict:%s" % y_predict)