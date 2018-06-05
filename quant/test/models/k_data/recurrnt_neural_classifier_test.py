# ae_h - 2018/6/5

import unittest
from datetime import datetime

from quant.dao.k_data.k_data_dao import k_data_dao
from quant.models.k_data.recurrent_neural_classifier import RecurrentNeurakClassifier
from quant.models.pca_model import PCAModel
from quant.test import before_run


class Recurrent_Neural_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'

        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        pac = PCAModel('k_data')
        pac.training_model(code=code, data=data, features=features)

        model = RecurrentNeurakClassifier()
        model.training_model(code, data, features)
