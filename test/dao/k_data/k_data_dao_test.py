import unittest

from dao.k_data.k_data_dao import k_data_dao

from test import before_run
from dao.data_source import dataSource


class K_Data_Dao_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_get_k_data(self):

        df = k_data_dao.get_k_data("SH.600196", start="2015-01-01", end="2018-05-27")
        self.assertIsNotNone(df)

    def tearDown(self):
        dataSource.futu_quote_ctx.close();

    '''
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

    '''