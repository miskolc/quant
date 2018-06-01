import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from quant.test import before_run
from quant.models.logistic_regression_classifier import LogisticRegressionClassifier
from quant.log.quant_logging import quant_logging as logging
from quant.dao.k_data_dao import k_data_dao
from quant.dao.index_k_data_dao import index_k_data_dao
from datetime import datetime

class Logistic_Regression_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600196'

        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logging.logger.debug("features:%s, length:%s" % (features, len(features)))

        model = LogisticRegressionClassifier()
        model.training_model(code ,data, features)

    def test_predict(self):
        code='600196'

        df_index = index_k_data_dao.get_rel_price();

        df,features = k_data_dao.get_k_predict_data_with_features(code, df_index)
        logging.logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = LogisticRegressionClassifier()
        y_predict = model.predict(code, df[features])

        print(y_predict)
