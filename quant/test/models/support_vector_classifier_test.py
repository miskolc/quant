import unittest
from datetime import datetime

from quant.dao.index_k_data_dao import index_k_data_dao
from quant.dao.k_data_dao import k_data_dao
from quant.log.quant_logging import logger
from quant.models.k_data.support_vector_classifier import SupportVectorClassifier
from quant.models.pca_model import PCAModel
from quant.test import before_run


class Support_Vector_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600276'
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logger.debug("features:%s" % features)

        pac = PCAModel();
        pac.training_model(code=code, data=data,features=features)

        model = SupportVectorClassifier()
        model.training_model(code, data, features)

    def test_predict(self):
        df_index = index_k_data_dao.get_rel_price();
        df, features = k_data_dao.get_k_predict_data_with_features("600196", df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = SupportVectorClassifier()
        y_predict = model.predict("600196", df[features])

        logger.debug("predict:%s" % y_predict)