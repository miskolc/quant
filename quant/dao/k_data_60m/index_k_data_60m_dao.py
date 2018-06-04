# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd
from quant.dao import cal_direction
from quant.crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts

class Index_K_Data_60m_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from index_k_data_60m "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        return df


    @exc_time
    def get_k_data_last_one(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from index_k_data_60m "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date desc limit 0,1")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        return df

    # 上证综合指数
    @exc_time
    def get_sh_k_data(self, start, end):
        return self.get_k_data('000001', start, end)

    # 深证成份指数
    @exc_time
    def get_sz_k_data(self, start, end):
        return self.get_k_data('399001', start, end)

    # 沪深300指数
    @exc_time
    def get_hs300_k_data(self, start, end):
        return self.get_k_data('000300', start, end)

    # 中证小盘500指数
    @exc_time
    def get_zz500_k_data(self, start, end):
        return self.get_k_data('000905', start, end)



index_k_data_60m_dao = Index_K_Data_60m_Dao()