import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

from quant.dao.data_source import dataSource
from quant.test import before_run
from quant.models.support_vector_classifier import SupportVectorClassifier
import pandas as pd
from quant.log.quant_logging import quant_logging as logging
from quant.dao.k_data_dao import k_data_dao
from datetime import datetime

def f(x):
    if x > 0:
        return 1
    elif x is None:
        return None
    else:
        return 0


class Support_Vector_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features("600196", '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logging.logger.debug("features:%s" % features)

        model = SupportVectorClassifier()
        model.training_model("600196", data, features)
