import unittest

from collector.k_data.k_data_collector import collect_all, collect_all_daily, collect_all_index, collect_all_index_daily, collect_single
from common_tools.datetime_utils import get_current_date
from config import default_config
from test import before_run
import futuquant as ft

class K_Data_Collector_Test(unittest.TestCase):


    def setUp(self):
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST, port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_collect_all(self):
        collect_all(self.futu_quote_ctx)

    def test_collect_single(self):
        collect_single(code='601668',futu_quote_ctx=self.futu_quote_ctx, start='2013-01-01', end=get_current_date())

    def test_collect_all_daily(self):
        collect_all_daily(self.futu_quote_ctx)

    def test_collect_all_index(self):
        collect_all_index(self.futu_quote_ctx)

    def test_collect_all_index_daily(self):
        collect_all_index_daily(self.futu_quote_ctx)
