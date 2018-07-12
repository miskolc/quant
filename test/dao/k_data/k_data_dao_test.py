import unittest

from dao import cal_direction
from dao.k_data.k_data_dao import k_data_dao

from dao.k_data.index_k_data_dao import index_k_data_dao
from log.quant_logging import logger
from test import before_run
import pandas as pd

class K_Data_Dao_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_get_k_data(self):

        df = k_data_dao.get_k_data("600196", start="2015-01-01", end="2018-05-27")
        self.assertIsNotNone(df)
        df.to_csv("result.csv")
        i = 1
        while i < 100:

            next_direction = df.iloc[i]["next_direction"]
            p_change = df.iloc[i + 1]["p_change"]

            # 如果next_direction ==0(代表跌), 检查下一日的p_change是否小于0
            # 验证next_direction是否正确
            if next_direction == 0:
                self.assertTrue(p_change <= 0)
            elif next_direction == 1:
                self.assertTrue(p_change > 0)

            i = i + 1

    def test_get_k_data_with_features(self):
        df, feature = k_data_dao.get_k_data_with_features("600000", start="2015-01-01", end="2018-06-30")
        df.to_csv("result.csv")
        logger.debug("features:%s" % feature)

    def test_get_k_predict_data_with_features(self):
        df_index = index_k_data_dao.get_rel_price();

        df, features = k_data_dao.get_k_predict_data_with_features('600000', df_index)
        print(features)
        df.to_csv("result.csv")
        logger.debug(df.tail())

    def test_rolling_tree_days(self):
        data = k_data_dao.get_k_data("600196", start="2018-06-01", end="2018-07-10", cal_next_direction=True)
        #next_3 = pd.Series(pd.Series.rolling(data['p_change'], 3).sum(), name='next_p_change_3')
        #data = data.join(next_3)
        #data['next_p_change_3'] = data['next_p_change_3'].shift(-3)
        #data['next_direction_3'] = data['next_p_change_3'].apply(cal_direction, i=0.03)
        print(data)

