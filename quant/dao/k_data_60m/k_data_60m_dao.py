# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import pandas as pd
from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.dao import cal_direction


class K_Data_60m_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_60m "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
        df['next_direction'] = df['p_change'].apply(cal_direction).shift(-1)
        df = df.dropna()
        return df


k_data_60m_dao = K_Data_60m_Dao()