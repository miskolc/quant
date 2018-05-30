# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.dao.k_data_tech_feature_dao import k_data_tech_feature_dao
import pandas as pd
from quant.feature_utils import adjust_features
from quant.dao.index_k_data_dao import index_k_data_dao

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

        df_sh = index_k_data_dao.get_sh_k_data(start, end)
        df = self.fill_index_feature(df, df_sh, 'sh_direction')

        df_sz = index_k_data_dao.get_sz_k_data(start, end)
        df = self.fill_index_feature(df, df_sz, 'sz_direction')

        df_hs300 = index_k_data_dao.get_hs300_k_data(start, end)
        df = self.fill_index_feature(df, df_hs300, 'hs300_direction')

        df_zz500 = index_k_data_dao.get_zz500_k_data(start, end)
        df = self.fill_index_feature(df, df_zz500, 'zz500_direction')

        df_gspc = index_k_data_dao.get_gspc_k_data(start, end)
        df = self.fill_index_feature(df, df_gspc, 'gspc_direction')

        df_hsi = index_k_data_dao.get_hsi_k_data(start, end)
        df = self.fill_index_feature(df, df_hsi, 'hsi_direction')

        df_ixic = index_k_data_dao.get_ixic_k_data(start, end)
        df = self.fill_index_feature(df, df_ixic, 'ixic_direction')

        df_feature = k_data_tech_feature_dao.get_k_data(code, start, end)
        features = list(df_feature.columns.values)

        df = pd.merge(df, df_feature, on=['date', 'code'])

        addition_features = ['open', 'close', 'low', 'high', 'sh_direction'
            ,'sz_direction','hs300_direction','zz500_direction','gspc_direction','hsi_direction','ixic_direction']
        features = adjust_features(features, addition_features)

        return df, features

    def fill_index_feature(self, df, df_sh, feature_name):
        df_sh[feature_name] = (df_sh['close'] - df_sh['pre_close']).apply(f)
        df = pd.merge(df, df_sh[['date', feature_name]], on=['date'], how="left")
        df = df.fillna(method="ffill")
        return df


k_data_dao = K_Data_Dao()