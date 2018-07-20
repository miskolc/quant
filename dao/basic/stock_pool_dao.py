# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7

import pandas as pd
import tushare as ts

from common_tools.decorators import exc_time
from dao.data_source import dataSource


class StockPoolDao:
    @exc_time
    def get_list(self):
        sql = ("select DISTINCT code, name from stock_pool where type='hs300'")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        #df['code'] = df['code'].apply(stock_pool_dao.fill_market)
        return df

    @exc_time
    def init_pool(self):

        df_zz = ts.get_zz500s()
        df_zz['type'] = 'zz500'
        df_hs300 = ts.get_hs300s()
        df_hs300['type'] = 'hs300'

        df_zz.to_sql('stock_pool', dataSource.mysql_quant_engine, if_exists='append', index=False)
        df_hs300.to_sql('stock_pool', dataSource.mysql_quant_engine, if_exists='append', index=False)




stock_pool_dao = StockPoolDao()