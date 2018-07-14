# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import pandas as pd
import tushare as ts
from dao import cal_direction
from dao.data_source import dataSource

from common_tools import exc_time


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

    @exc_time
    def get_rel_price(self):
        df_index = ts.get_index()
        # 上证指数
        df_sh = df_index[df_index["code"] == '000001']
        df_sz = df_index[df_index["code"] == '399001']
        df_hs300 = df_index[df_index["code"] == '000300']
        df_zz500 = df_index[df_index["code"] == '000905']

        dict = [{
            'sh_direction': cal_direction(float(df_sh["change"].values[0])),
            'sz_direction': cal_direction(float(df_sz["change"].values[0])),
            'hs300_direction': cal_direction(float(df_hs300["change"].values[0])),
            'zz500_direction': cal_direction(float(df_zz500["change"].values[0]))
        }]

        df = pd.DataFrame(dict)

        return df


index_k_data_60m_dao = Index_K_Data_60m_Dao()