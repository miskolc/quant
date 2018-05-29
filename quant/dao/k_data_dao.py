# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.dao.k_data_tech_feature_dao import k_data_tech_feature_dao
import pandas as pd
from quant.feature_utils import adjust_features

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
                         , con=dataSource.mysql_quant_engine)

        df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
        df['next_direction'] = df['p_change'].apply(f).shift(-1)
        df = df.dropna()
        return df

    def get_k_data_with_features(self, code, start, end):
        df = self.get_k_data(code, start, end)
        df_feature = k_data_tech_feature_dao.get_k_data(code, start, end)
        features = list(df_feature.columns.values)

        features = adjust_features(features)

        df = pd.merge(df, df_feature, on=['date', 'code'])

        return df, features


k_data_dao = K_Data_Dao()