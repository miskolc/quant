import unittest
from quant.crawler.jqka_finance_api import jqka_finance_api
from quant.common_tools.datetime_utils import get_next_date, get_current_date
from datetime import datetime, timedelta
import numpy as np

class JQKA_Finance_Api_Test(unittest.TestCase):


    def test_get_stock_performance(self):
        df = jqka_finance_api.get_data()
        jqka_finance_api.read_data(df,)
        #df = jqka_finance_api.get_stock_performance(code=code)
        #print(df)

