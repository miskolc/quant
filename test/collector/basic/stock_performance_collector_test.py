import unittest

from collector.basic.stock_basic_collector import collect_stock_basic
from test import before_run


class Stock_Basic__Test(unittest.TestCase):
    def setUp(self):
        before_run()


    def test_collect_stock_basic(self):
        collect_stock_basic()