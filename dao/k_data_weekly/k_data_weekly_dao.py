# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools.decorators import exc_time

from dao.k_data import fill_market


class K_Data_Weekly_Dao:
    @exc_time
    def get_k_data(self, code, start, end, futu_quote_ctx):

        state, data = futu_quote_ctx.get_history_kline(fill_market(code), ktype='K_WEEK', autype='qfq', start=start,end=end)

        return data

    @exc_time
    def get_multiple_history_kline(self, code_list, start, end, futu_quote_ctx):
        code_list = list(map(fill_market, code_list))

        state, data = futu_quote_ctx.get_multiple_history_kline(codelist=code_list
                                                                , start=start, end=end,  ktype='K_WEEK', autype='qfq')

        k_data_dict = {}
        for item in data:
            if item is None or len(item["code"]) <=0:
                continue

            code = item["code"].tail(1).values[0]
            k_data_dict[code] = item

        return k_data_dict

    '''
    @exc_time
    def get_k_data_all(self):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_weekly ")

        df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn)
        df = df.dropna()
        return df
    '''


k_data_weekly_dao = K_Data_Weekly_Dao()
