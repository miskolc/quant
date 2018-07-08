# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from datetime import datetime, timedelta

import pandas as pd
import tushare as ts
from quant.dao.k_data.k_data_tech_feature_dao import k_data_tech_feature_dao

from quant.common_tools.decorators import exc_time
from quant.dao import cal_direction
from quant.dao.data_source import dataSource
from quant.dao.k_data.index_k_data_dao import index_k_data_dao
from quant.feature_utils import adjust_features
from quant.feature_utils.feature_collector import collect_features
from quant.dao.basic.stock_structure_dao import stock_structure_dao


class K_Data_Week_Dao:

    @exc_time
    def get_k_data(self, code, start, end, cal_next_direction=False):
        sql = ('''select  k.`date`,  k.code,  k.open,  k.close,  k.high,  k.low,  k.volume,  k.pre_close
               from k_data_week k 
               where k.code=%(code)s and k.date BETWEEN %(start)s and %(end)s order by k.date asc ''')

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def get_k_data_all(self):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_week ")

        df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn)
        df = df.dropna()
        return df


k_data_week_dao = K_Data_Week_Dao()
