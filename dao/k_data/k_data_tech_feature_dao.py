# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools import exc_time
from dao.data_source import dataSource
import pandas as pd
from sqlalchemy.sql import text


class K_Data_Tech_Feature_Dao:
    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select * from k_data_tech_feature "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        df = df.drop(columns=['createTime'])

        return df

    def update_single_column(self, code, column, value):
        sql = text('update k_data_tech_feature set :column=:value where code=:code')

        dataSource.mysql_quant_conn.execute(sql, code=code, column=column, value=value)


k_data_tech_feature_dao = K_Data_Tech_Feature_Dao()
