# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd
from quant.dao import cal_direction
from quant.crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts


class StockPerformanceDao:
    @exc_time
    def get_by_code(self, code, year, quarter):
        sql = ("select `code`, eps, eps_yoy, bvps, roe, epcf, net_profits, profits_yoy from stock_performance "
               "where code=%(code)s and year=%(year)s and quarter=%(quarter)s")

        df = pd.read_sql(sql=sql, params={"code": code, "year": year, "quarter": quarter}
                         , con=dataSource.mysql_quant_conn)

        df = df.fillna(0)

        return df

stock_performance_dao = StockPerformanceDao()