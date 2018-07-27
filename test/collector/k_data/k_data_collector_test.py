import unittest

from collector.k_data.k_data_collector import collect_all,collect_all_daily
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

    def test_collect_all_daily(self):
        collect_all_daily(self.futu_quote_ctx)

