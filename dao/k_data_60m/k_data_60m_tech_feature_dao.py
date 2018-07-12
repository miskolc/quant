# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools import exc_time
from dao.data_source import dataSource
import pandas as pd



class K_Data_60m_Tech_Feature_Dao:

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select * from k_data_60m_tech_feature "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        df = df.drop(columns=['createTime'])

        return df




k_data_60m_tech_feature_dao = K_Data_60m_Tech_Feature_Dao()