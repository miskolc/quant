# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd
from quant.dao import cal_direction
from quant.crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts

class Index_K_Data_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from index_k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_engine)

        return df


    @exc_time
    def get_k_data_last_one(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from index_k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date desc limit 0,1")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_engine)

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

    # 恒生指數
    @exc_time
    def get_hsi_k_data(self, start, end):
        return self.get_k_data('^HSI', start, end)

    #  納斯達克指數: ^IXIC
    @exc_time
    def get_ixic_k_data(self, start, end):
        return self.get_k_data('^HSI', start, end)

    # 标普500: ^GSPC
    @exc_time
    def get_gspc_k_data(self, start, end):
        return self.get_k_data('^GSPC', start, end)

    # 道琼斯指数: ^DJI
    @exc_time
    def get_gspc_k_data(self, start, end):
        return self.get_k_data('^DJI', start, end)

    @exc_time
    def get_rel_price(self):
        df_index = ts.get_index()
        # 上证指数
        df_sh = df_index[df_index["code"] == '000001']
        df_sz = df_index[df_index["code"] == '399001']
        df_hs300 = df_index[df_index["code"] == '000300']
        df_zz500 = df_index[df_index["code"] == '000905']


        hsi_price, hsi_pre_close = yahoo_finance_api.get_real_price('^HSI')
        gspc_price, gspc_pre_close = yahoo_finance_api.get_real_price('^GSPC')
        ixic_price, ixic_pre_close = yahoo_finance_api.get_real_price('^IXIC')

        dict =[{
            'sh_direction' : cal_direction(float(df_sh["change"].values[0])),
            'sz_direction' : cal_direction(float(df_sz["change"].values[0])),
            'hs300_direction' : cal_direction(float(df_hs300["change"].values[0])),
            'zz500_direction' :  cal_direction(float(df_hs300["change"].values[0])),
            'hsi_direction' : cal_direction(hsi_price - hsi_pre_close),
            'gspc_direction' : cal_direction(gspc_price - gspc_pre_close),
            'ixic_direction' : cal_direction(ixic_price - ixic_pre_close)
        }]

        df = pd.DataFrame(dict)

        return df

index_k_data_dao = Index_K_Data_Dao()