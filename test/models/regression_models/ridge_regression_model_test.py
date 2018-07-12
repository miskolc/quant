# ae_h - 2018/6/6
import unittest
from datetime import datetime

from dao.k_data_60m.k_data_60m_dao import k_data_60m_dao
from log.quant_logging import logger
from models.regression_models.ridge_regression_model import RidgeRegressionModel
from test import before_run

from models.pca_model import PCAModel


class Ridge_Regression_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'
        data, features = k_data_60m_dao.get_k_data_with_features(code, '2015-01-01',
                                                             datetime.now().strftime("%Y-%m-%d"))

        logger.debug("features:%s, length:%s" % (features, len(features)))

        pac = PCAModel('k_data')
        pac.training_model(code=code, data=data, features=features)

        model = RidgeRegressionModel()
        model.training_model(code, data, features)