# coding = utf-8
# ae_h - 2018/5/29

import unittest
from quant.models.sequantial_neural import SequantialNeural
from quant.test import before_run
from quant.dao.k_data_dao import k_data_dao
from quant.models.pca_model import PCAModel
from quant.common_tools import datetime_utils


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