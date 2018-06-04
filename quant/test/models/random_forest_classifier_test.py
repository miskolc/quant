# coding = utf-8
# ae_h - 2018/5/30

import unittest
from datetime import datetime

from quant.dao.k_data.k_data_dao import k_data_dao

from quant.dao.k_data.index_k_data_dao import index_k_data_dao
from quant.log.quant_logging import logger
from quant.models.k_data.random_forest_classifier import RandomForestClassifierModel
from quant.models.pca_model import PCAModel
from quant.test import before_run


class Random_Forest_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'

        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        pac = PCAModel();
        pac.training_model(code=code, data=data, features=features)

        model = RandomForestClassifierModel()
        model.training_model(code, data, features)

    def test_predict(self):
        df_index = index_k_data_dao.get_rel_price();
        df, features = k_data_dao.get_k_predict_data_with_features("600196", df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = RandomForestClassifierModel()
        y_predict = model.predict("600196", df[features])

        logger.debug("predict:%s" % y_predict)