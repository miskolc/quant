import unittest
from quant.test import before_run
from quant.collector.basic import stock_structure_collector
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.dao.basic.stock_structure_dao import stock_structure_dao

class Stock_Structure_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_structure(self):
        stock_structure_collector.collect_all();

    def test_fill_k_data(self):
        code = '603799'
        data = k_data_dao.get_k_data(code, start='2015-01-01', end='2018-06-01')
        data = stock_structure_dao.fill_stock_structure(code, data)
        data.to_csv('result.csv')

    def test_collect_single(self):
        stock_structure_collector.collect_single('600074')