# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools.decorators import exc_time
from dao.data_source import dataSource


class K_Data_Weekly_Dao:
    @exc_time
    def get_k_data(self, code, start=None, end=None):
        state, data = dataSource.futu_quote_ctx.get_history_kline(code, ktype='K_WEEK', autype='qfq', start=start,
                                                                  end=end)
        return data

    '''
    @exc_time
    def get_k_data_all(self):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_weekly ")

        df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn)
        df = df.dropna()
        return df
    '''


k_data_weekly_dao = K_Data_Weekly_Dao()
