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
    def get_by_code(self, code, start, end):
        sql = ("select `code`, eps, eps_yoy, bvps, roe, epcf, net_profits, profits_yoy, report_date as date from stock_performance "
               "where code=%(code)s and report_date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        df = df.fillna(0)

        return df

stock_performance_dao = StockPerformanceDao()