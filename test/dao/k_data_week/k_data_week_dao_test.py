import unittest

from config import default_config
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
import futuquant as ft


class K_Data_Week_Dao_Test(unittest.TestCase):


    def test_get_k_data(self):
        df = k_data_weekly_dao.get_k_data('600196', start=None, end=None)

        #df.to_csv("result.csv")
        print(df)

    def test_get_multiple_k_data(self):

        df = k_data_weekly_dao.get_multiple_k_data(code_list = ["601398", '600196', '000001'], start="2018-07-02", end="2018-07-28")
        print(df)
        self.assertIsNotNone(df)