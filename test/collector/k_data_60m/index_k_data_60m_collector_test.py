import unittest
from test import before_run
import collector.k_data_60m.index_k_data_60m_collector as index_k_data_60m_collector
import tushare as ts
from log.quant_logging import logger


class Index_K_Data_60m_Test(unittest.TestCase):
    def setUp(self):
        before_run()



    def test_collect_hs300_daily(self):
        index_k_data_60m_collector.collect_index_china_daily()