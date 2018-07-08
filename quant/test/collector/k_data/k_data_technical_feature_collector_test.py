import unittest
from quant.collector.k_data.k_data_technical_feature_collector import collect_full,collect_single
from quant.test import before_run

class K_Data_Technical_Feature_Collector_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_full(self):
        collect_full()


    def test_collect_single(self):
        collect_single('600073', '2015-01-01', '2018-07-06')