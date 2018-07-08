import unittest
from quant.collector.k_data.k_data_technical_feature_collector import collect_hs300_full,collect_single_daily, collect_single, collect_hs300_daily
from quant.test import before_run

class K_Data_Technical_Feature_Collector_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_hs300_full(self):
        collect_hs300_full()


    def test_collect_single(self):
        collect_hs300_daily()