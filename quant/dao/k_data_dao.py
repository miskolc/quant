# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.dao.k_data_tech_feature_dao import k_data_tech_feature_dao
import pandas as pd
from quant.feature_utils import adjust_features
from quant.dao.index_k_data_dao import index_k_data_dao
import tushare as ts
from quant.log.quant_logging import quant_logging as logging
from quant.dao import cal_direction
from datetime import datetime,timedelta



class K_Data_Dao:
    @staticmethod
    def get_addition_features():
        return ['open', 'close', 'low', 'high', 'volume', 'sh_direction'
            , 'sz_direction', 'hs300_direction', 'zz500_direction',
                'gspc_direction', 'hsi_direction', 'ixic_direction']

    @exc_time
    def get_k_data(self, code, start, end):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data "
               "where code=%(code)s and date BETWEEN %(start)s and %(end)s order by date asc")

        logging.logger.debug("sql:" + sql)
        df = pd.read_sql(sql=sql, params={"code": code, "start": start, "end": end}
                         , con=dataSource.mysql_quant_engine)

        df['p_change'] = ((df['close'] - df['pre_close']) / df['pre_close'])
        df['next_direction'] = df['p_change'].apply(cal_direction).shift(-1)
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

        features = adjust_features(features, self.get_addition_features())

        return df, features

    def fill_index_feature(self, df, df_sh, feature_name):
        df_sh[feature_name] = (df_sh['close'] - df_sh['pre_close']).apply(cal_direction)
        df = pd.merge(df, df_sh[['date', feature_name]], on=['date'], how="left")
        df = df.fillna(method="ffill")
        return df

    # 集成今日的预测数据
    def get_k_predict_data_with_features(self, code, df_index):
        now = datetime.now().strftime('%Y-%m-%d')
        print(now)
        last_60 = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')

        df = self.get_k_data(code, start=last_60, end=now)
        df.to_csv('result.csv')
        df_real = ts.get_realtime_quotes(code)
        df_real = df_real[['open','price','low', 'high', 'volume']]
        df_real = df_real.rename(columns={'price': 'close'})
        df_real['date'] = now

        df = df.append(df_real)




        logging.logger.debug(df.tail())


k_data_dao = K_Data_Dao()
