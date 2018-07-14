import unittest
from collector.k_data.k_data_technical_feature_collector import collect_full,collect_single, collect_single_daily
from test import before_run

class K_Data_Technical_Feature_Collector_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_full(self):
        collect_full()


    def test_collect_single(self):
        collect_single('002466', '2018-01-01', '2018-07-06')

    def test_collect_single(self):
        collect_single_daily('002466')