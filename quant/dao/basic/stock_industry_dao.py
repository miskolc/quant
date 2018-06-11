# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd
from quant.dao import cal_direction
from quant.crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts


class StockIndustryDao:
    @exc_time
    def get_list(self):
        sql = ("select `bk_code`, bk_name, code, name from stock_industry ")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

stock_industry_dao = StockIndustryDao()