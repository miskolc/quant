# ae_h - 2018/6/1
import unittest
from datetime import datetime

from quant.dao.index_k_data_dao import index_k_data_dao
from quant.dao.k_data_dao import k_data_dao
from quant.log.quant_logging import quant_logging as logging
from quant.models.pca_model import PCAModel
from quant.models.xgboost_classifier import XGBoostClassier
from quant.test import before_run


def f(x):
    if x > 0:
        return 1
    elif x is None:
        return None
    else:
        return 0


class XGBoost_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        code = '600519'
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logging.logger.debug("features:%s" % features)

        pac = PCAModel()
        pac.training_model(code=code, data=data,features=features)

        model = XGBoostClassier()
        model.training_model(code, data, features)

    # def test_predict(self):
    #     df_index = index_k_data_dao.get_rel_price()
    #     df, features = k_data_dao.get_k_predict_data_with_features("600196", df_index)
    #     logging.logger.debug("features:%s, length:%s" % (features, len(features)))
    #
    #     df.to_csv("result.csv")
    #     model = XGBoostClassier()
    #     y_predict = model.predict("600196", df[features])
    #
    #     print(y_predict)