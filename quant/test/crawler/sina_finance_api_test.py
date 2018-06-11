import unittest
from quant.crawler.sina_finance_api import sina_finance_api
from quant.common_tools.datetime_utils import get_next_date, get_current_date
from datetime import datetime, timedelta
import numpy as np

class Sina_Finance_Api_Test(unittest.TestCase):


    def test_01(self):
        df = sina_finance_api.get_stock_structure_by_code('600196')
        print(df)
