import unittest

#from collector.k_data.k_data_stock_performance_collector import collect_quarter, collect_quarter_all
from test import before_run
import tushare as ts


class Stock_Performance_Classified_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_quarter_all(self):
        #collect_quarter_all('2018-01-01', '2018-03-31', 2017, 4)
        pass


    def collect_single_daily(self):
        data_report = ts.get_report_data(2018, 2)
        data_report.to_csv('result.csv')
        #collect_quarter(data_report, '600000', '2018-06-12', '2018-06-12')
        print(data_report)

    def test_collect_quarter(self):
        pass
        #collect_quarter(code='600000', start='2018-04-01', end='2018-06-30', year=2018, quarter=1)

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
