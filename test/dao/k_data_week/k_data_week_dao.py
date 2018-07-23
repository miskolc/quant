import unittest

from config import default_config
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
import futuquant as ft

class K_Data_Week_Dao_Test(unittest.TestCase):

    def setUp(self):

        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                  port=default_config.FUTU_OPEND_PORT)


    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_get_k_data(self):
        df = k_data_weekly_dao.get_k_data('600196',start=None, end=None, futu_quote_ctx=self.futu_quote_ctx)

        df.to_csv("result.csv")



