# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
import pandas as pd


class K_Data_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume from k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_engine)

        return df


k_data_dao = K_Data_Dao()