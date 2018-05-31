import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from quant.test import before_run
from quant.models.logistic_regression_classifier import LogisticRegressionClassifier
from quant.log.quant_logging import quant_logging as logging
from quant.dao.k_data_dao import k_data_dao
from datetime import datetime

class Logistic_Regression_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features("600196", '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logging.logger.debug("features:%s" % features)

        model = LogisticRegressionClassifier()
        model.training_model("600196" ,data, features)
