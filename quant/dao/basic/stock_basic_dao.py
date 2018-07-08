# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7
import pandas as pd
from sqlalchemy.sql import text

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource


class StockBasicDao:
    @exc_time
    def get_by_code(self, code, year, quarter):
        sql = ("select `code`, eps, pb, pe, roe, income_yoy, profits_yoy from stock_basic "
               "where code=%(code)s ")

        df = pd.read_sql(sql=sql, params={"code": code, "year": year, "quarter": quarter}
                         , con=dataSource.mysql_quant_conn)

        df = df.fillna(0)

        return df

    @exc_time
    def truncate(self):
        sql = text('truncate table stock_basic')
        dataSource.mysql_quant_conn.execute(sql)


stock_basic_dao = StockBasicDao()