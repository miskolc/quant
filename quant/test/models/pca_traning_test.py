# coding = utf-8
# ae_h - 2018/6/1

import unittest
from datetime import datetime

from quant.dao.k_data.k_data_dao import k_data_dao
from quant.models.pca_model import PCAModel
from quant.test import before_run


class PcaTrainingTest(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        data, features = k_data_dao.get_k_data_with_features('600196', '2015-01-01',
                                                             datetime.now().strftime("%Y-%m-%d"))

        pca_model = PCAModel('k_data')

        pca_model.training_model(code='600196', data=data, features=features)
