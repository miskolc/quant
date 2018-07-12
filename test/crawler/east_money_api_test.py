import unittest
from crawler.east_money_api import east_money_api


class East_Money_Api_Test(unittest.TestCase):


    def test_get_stock_basic(self):
        df = east_money_api.get_stock_basic('600196')
        print(df)
