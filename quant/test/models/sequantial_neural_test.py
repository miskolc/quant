# coding = utf-8
# ae_h - 2018/5/29

import unittest
from quant.models.sequantial_neural import SequantialNeural
from quant.test import before_run
from quant.dao.k_data_dao import k_data_dao
from quant.models.pca_model import PCAModel
from quant.common_tools import datetime_utils
from quant.dao.index_k_data_dao import index_k_data_dao
from quant.log.quant_logging import quant_logging as logging

class Sequantial_Neural_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'

        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime_utils.get_current_date())

        pac = PCAModel();
        pac.training_model(code=code, data=data, features=features)

        model = SequantialNeural()
        model.training_model(code, data, features)

    def test_predict(self):
        df_index = index_k_data_dao.get_rel_price();
        df, features = k_data_dao.get_k_predict_data_with_features("600196", df_index)
        logging.logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = SequantialNeural()
        y_predict = model.predict("600196", df[features])

        logging.logger.debug("predict:%s"%y_predict)