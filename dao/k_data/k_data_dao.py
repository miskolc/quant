# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19
from functools import lru_cache

from common_tools.decorators import exc_time
from dao import cal_direction
from dao.k_data import fill_market

'''
    HS300指数: SH.000300

'''


class K_Data_Dao:
    @exc_time
    def get_k_data(self, code, start, end, futu_quote_ctx):

        state, data = futu_quote_ctx.get_history_kline(fill_market(code), ktype='K_DAY', autype='qfq', start=start,end=end)

        return data

    @exc_time
    def get_trading_days(self, start, end, futu_quote_ctx, market='SH'):

        state, data = futu_quote_ctx.get_trading_days(market, start_date=start, end_date=end)

        return data

    @exc_time
    def get_multiple_history_kline(self, code_list, start, end, futu_quote_ctx):
        code_list = list(map(fill_market, code_list))

        state, data = futu_quote_ctx.get_multiple_history_kline(codelist=code_list
                                                                , start=start, end=end,  ktype='K_DAY', autype='qfq')
        return data


    def get_k_training_data(self, code, start, end, futu_quote_ctx):

        state, data = futu_quote_ctx.get_history_kline(fill_market(code), ktype='K_DAY', autype='qfq', start=start,end=end)

        data['next_direction'] = data['change_rate'].apply(cal_direction).shift(-1)

        feature = ['open','close', 'high', 'low', 'pe_ratio', 'turnover_rate', 'volume']

        data = data.dropna()

        return data, feature

    '''
    @staticmethod
    def get_addition_index_features():
        return ['sh_direction', 'sz_direction', 'hs300_direction', 'zz500_direction',
                'gspc_direction', 'hsi_direction', 'ixic_direction']

    @staticmethod
    def get_addition_features():
        features = ['open', 'close', 'low', 'high', 'volume']

        features.extend(K_Data_Dao.get_addition_index_features())

        return features
    
    @exc_time
    def get_k_data_all(self):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data ")

        df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn)
        df = df.dropna()
        return df

    @exc_time
    def get_k_data_with_features(self, code, start, end):
        df = self.get_k_data(code, start, end, cal_next_direction=True)

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

        df = df.dropna()

        features = adjust_features(features, self.get_addition_features())

        return df, features

    def fill_index_feature(self, df, df_sh, feature_name):
        df_sh[feature_name] = (df_sh['close'] - df_sh['pre_close']).apply(cal_direction)
        df = pd.merge(df, df_sh[['date', feature_name]], on=['date'], how="left")
        df = df.fillna(method="ffill")
        return df

    # 集成今日的预测数据
    @exc_time
    def get_k_predict_data_with_features(self, code, df_index):
        now = datetime.now().strftime('%Y-%m-%d')

        last_60 = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')

        df = self.get_k_data(code, start=last_60, end=now, cal_next_direction=False)
        df = df[['open', 'close', 'low', 'high', 'volume']]

        df_real = ts.get_realtime_quotes(code)

        df_real = df_real[['open', 'price', 'low', 'high', 'volume']].astype('float64')
        df_real = df_real.rename(columns={'price': 'close'})
        df_real['volume'] = df_real['volume'] / 100
        df = pd.concat([df, df_real], axis=0, ignore_index=True)

        df, features = collect_features(df)

        # 获取今天要预测的最后一行
        df = df.tail(1)
        df = df.reset_index(drop=True)

        # 拼接上指数
        df = pd.concat([df, df_index], axis=1)

        features = adjust_features(features, self.get_addition_features())

        return df, features
    '''


k_data_dao = K_Data_Dao()
