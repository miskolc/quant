# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/05

import pandas as pd
from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.dao import cal_direction
from quant.dao.k_data_60m.index_k_data_60m_dao import index_k_data_60m_dao
from quant.dao.k_data_60m.k_data_60m_tech_feature_dao import k_data_60m_tech_feature_dao
from quant.feature_utils import adjust_features


class K_Data_60m_Dao:
    @exc_time
    def get_k_data(self, code, start, end, cal_next_direction=True):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_60m "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_conn)

        df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])

        if cal_next_direction:
            df['next_direction'] = df['p_change'].apply(cal_direction).shift(-1)
            df = df.dropna()
        return df

    def fill_index_feature(self, df, df_sh, feature_name):
        df_sh[feature_name] = (df_sh['close'] - df_sh['pre_close']).apply(cal_direction)
        df = pd.merge(df, df_sh[['date', feature_name]], on=['date'], how="left")
        df = df.fillna(method="ffill")
        return df

    @staticmethod
    def get_addition_index_features():
        return ['sh_direction', 'sz_direction', 'hs300_direction', 'zz500_direction',]

    @staticmethod
    def get_addition_features():
        features = ['open', 'close', 'low', 'high', 'volume']

        features.extend(K_Data_60m_Dao.get_addition_index_features())

        return features

    def get_k_data_with_features(self, code, start, end):
        df = self.get_k_data(code, start, end)

        df_sh = index_k_data_60m_dao.get_sh_k_data(start, end)
        df = self.fill_index_feature(df, df_sh, 'sh_direction')

        df_sz = index_k_data_60m_dao.get_sz_k_data(start, end)
        df = self.fill_index_feature(df, df_sz, 'sz_direction')

        df_hs300 = index_k_data_60m_dao.get_hs300_k_data(start, end)
        df = self.fill_index_feature(df, df_hs300, 'hs300_direction')

        df_zz500 = index_k_data_60m_dao.get_zz500_k_data(start, end)
        df = self.fill_index_feature(df, df_zz500, 'zz500_direction')

        df_feature = k_data_60m_tech_feature_dao.get_k_data(code, start, end)
        features = list(df_feature.columns.values)

        df = pd.merge(df, df_feature, on=['date', 'code'])

        features = adjust_features(features, self.get_addition_features())

        return df, features


k_data_60m_dao = K_Data_60m_Dao()
