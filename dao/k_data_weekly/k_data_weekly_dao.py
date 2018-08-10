# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19
import datetime

from sqlalchemy import text

from common_tools.datetime_utils import get_current_date, DATE_FORMAT
from common_tools.decorators import exc_time
from dao import dataSource
import pandas as pd
from dao.k_data import fill_market


class K_Data_Weekly_Dao:
    @exc_time
    def get_k_data(self, code, start, end):

        if start is None:
            start = '2013-01-01'

        if end is None:
            end = get_current_date()

        sql = ('''select  *
                 from k_data_weekly  
                 where code=%(code)s and time_key BETWEEN %(start)s and %(end)s order by time_key asc ''')

        data = pd.read_sql(sql=sql, params={"code": fill_market(code), "start": start, "end": end}
                           , con=dataSource.mysql_quant_conn)

        return data

    @exc_time
    def get_multiple_k_data(self, code_list, start=None, end=None):

        if start is None:
            start = '2013-01-01'

        if end is None:
            end = get_current_date()

        sql = ('''select  *
                 from k_data_weekly  
                 where code in %(code_list)s and time_key BETWEEN %(start)s and %(end)s order by time_key asc ''')

        codes_list = [fill_market(code) for code in code_list]

        data = pd.read_sql(sql=sql, params={"code_list": codes_list, "start": start, "end": end}
                           , con=dataSource.mysql_quant_conn)

        return data


    @exc_time
    def delete_current_week_k_data(self):
        today = datetime.date.today()
        monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
        monday = monday.strftime(DATE_FORMAT)

        sql = text('delete from k_data_weekly where time_key=:time_key')
        dataSource.mysql_quant_conn.execute(sql, time_key=monday)


    '''
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



    
    @exc_time
    def get_k_data_all(self):
        sql = ("select `date`, code, open, close, high, low, volume, pre_close from k_data_weekly ")

        df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn)
        df = df.dropna()
        return df
    '''


k_data_weekly_dao = K_Data_Weekly_Dao()
