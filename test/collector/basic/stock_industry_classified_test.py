import unittest

from crawler.east_money_api import east_money_api
from dao.data_source import dataSource
from test import before_run
from collector.basic import stock_industry_collector


class Stock_Industry_Classified_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_industry(self):
        stock_industry_collector.collect_all();


    def test_collect_industry_single(self):
        data = east_money_api.get_stock_industry_by_bk_code('BK0696', '国产软件')
        data.to_sql('stock_industry', dataSource.mysql_quant_engine, if_exists='append', index=False)

        print(data)