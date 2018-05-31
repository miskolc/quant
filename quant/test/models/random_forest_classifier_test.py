# coding = utf-8
# ae_h - 2018/5/30

import unittest
from quant.models.random_forest_classifier import RandomForestClassifierModel
from quant.test import before_run
from quant.log.quant_logging import quant_logging as logging
from quant.dao.k_data_dao import k_data_dao
from datetime import datetime

class Random_Forest_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):

        data, features = k_data_dao.get_k_data_with_features("000568", '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        model = RandomForestClassifierModel()
        model.training_model("000568", data, features)
