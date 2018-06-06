# ae_h - 2018/6/5
import unittest
from datetime import datetime

from quant.dao.k_data.k_data_dao import k_data_dao
from quant.models.regression_models.linear_regression_model import LinearRegressionModel
from quant.log.quant_logging import logger
from quant.models.pca_model import PCAModel
from quant.test import before_run


class Linear_Regression_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'
        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01',
                                                             datetime.now().strftime("%Y-%m-%d"))

        logger.debug("features:%s, length:%s" % (features, len(features)))

        pac = PCAModel('k_data')
        pac.training_model(code=code, data=data,features=features)

        model = LinearRegressionModel()
        model.training_model(code, data, features)