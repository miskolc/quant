# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd


class Index_K_Data_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from index_k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

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

index_k_data_dao = Index_K_Data_Dao()