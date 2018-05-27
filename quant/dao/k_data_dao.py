# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd


def f(x):
    if x > 0:
        return 1
    elif x is None:
        return None
    else:
        return 0

class K_Data_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_engine, index_col=["date"])

        df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
        df['next_direction'] = df['p_change'].apply(f).shift(-1)
        df = df.dropna()
        return df




k_data_dao = K_Data_Dao()