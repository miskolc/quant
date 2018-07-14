import unittest
from crawler.sina_finance_api import sina_finance_api


class Sina_Finance_Api_Test(unittest.TestCase):


    def test_01(self):
        df = sina_finance_api.get_stock_structure_by_code('600196')
        print(df)
