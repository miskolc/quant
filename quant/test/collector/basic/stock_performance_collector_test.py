import unittest

from quant.collector.basic.stock_basic_collector import  collect_stock_basic
from quant.test import before_run
import tushare as ts

class Stock_Basic__Test(unittest.TestCase):
    def setUp(self):
        before_run()



        '''
        collect_quarter_all(2017, 4, '2018-01-01', '2018-03-31')
        collect_quarter_all(2017, 3, '2017-10-01', '2017-12-31')
        collect_quarter_all(2017, 2, '2017-7-01', '2017-9-31')
        collect_quarter_all(2017, 1, '2017-4-01', '2017-6-30')

        collect_quarter_all(2016, 4, '2017-01-01', '2017-03-31')
        collect_quarter_all(2016, 3, '2016-10-01', '2016-12-31')
        collect_quarter_all(2016, 2, '2016-7-01', '2016-9-31')
        collect_quarter_all(2016, 1, '2016-4-01', '2016-6-30')

        collect_quarter_all(2015, 4, '2016-01-01', '2016-03-31')
        collect_quarter_all(2015, 3, '2015-10-01', '2015-12-31')
        collect_quarter_all(2015, 2, '2015-7-01', '2015-9-31')
        collect_quarter_all(2015, 1, '2015-4-01', '2015-6-30')
'''
        '''
        collect_single_quarter(2015, 2)
        collect_single_quarter(2015, 3)
        collect_single_quarter(2015, 4)
        collect_single_quarter(2016, 1)
        collect_single_quarter(2016, 2)
        collect_single_quarter(2016, 3)
        collect_single_quarter(2016, 4)
        collect_single_quarter(2017, 1)
        collect_single_quarter(2017, 2)
        collect_single_quarter(2017, 3)
        collect_single_quarter(2017, 4)
        collect_single_quarter(2018, 1)
        2727
        '''


    def test_collect_stock_basic(self):
        collect_stock_basic()