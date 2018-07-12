import unittest
from crawler.yahoo_finance_api import yahoo_finance_api
from common_tools import get_next_date, get_current_date
from datetime import datetime, timedelta
from feature_utils.feature_collector import collect_features
import numpy as np

class Yahoo_Finance_Api_Test(unittest.TestCase):


    def test_01(self):
        start = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')
        end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        code = 'AAPL'

        data = yahoo_finance_api.get_k_data(code, start_date=start, end_date=end)
        data["volume"] = data["volume"].astype('float64')
        data, f = collect_features(data)

        data.to_csv("result.csv")
