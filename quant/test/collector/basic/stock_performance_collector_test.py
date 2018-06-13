import unittest

from quant.collector.basic.stock_performance_collector import collect_quarter_all,cal_quarter_by_date, collect_single
from quant.test import before_run
import tushare as ts

class Stock_Performance_Classified_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def collect_single(self):
        data_report = ts.get_report_data(2018, 1)
        collect_single(data_report, '600000','2018-04-01', '2018-06-30')
        

    def collect_single_daily(self):
        data_report = ts.get_report_data(2018, 1)
        collect_single(data_report, '600000','2018-06-12', '2018-06-12')

    def collect_all(self):
        collect_quarter_all(2018, 1, '2018-04-01', '2018-06-30')

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
        '''

    def test_cal_quarter_by_date(self):
        print(cal_quarter_by_date('2018-06-13'))
