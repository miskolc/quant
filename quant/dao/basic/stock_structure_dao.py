# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd
from quant.dao import cal_direction
from quant.crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts


class StockStructureDao:
    @exc_time
    def get_stock_structure_list(self):
        sql = ("select `code`, name, share_oustanding from stock_structure ")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def get_stock_structure_by_code(self, code):
        sql = ("select `code`, name, share_oustanding,date from stock_structure where code=%(code)s")

        df = pd.read_sql(sql=sql, params={"code": code}
                         , con=dataSource.mysql_quant_conn)

        return df

    def fill_stock_structure(self, code, data):
        df_ss = self.get_stock_structure_by_code(code)
        so_arr = []

        for index, row in data.iterrows():
            df_sso = df_ss[df_ss['date'] < row['date']].tail(1)
            so_arr.append(df_sso['share_oustanding'].values[0])

        data["share_oustanding"] = so_arr

        return data


stock_structure_dao = StockStructureDao()
