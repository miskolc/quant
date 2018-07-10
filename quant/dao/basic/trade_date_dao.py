import datetime

import pandas as pd
import tushare as ts

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource


class Trade_Date_Dao:
    '''
            判断是否为交易日，返回True or False
    '''

    @exc_time
    def is_holiday(self, date):

        df = self.trade_cal()

        holiday = df[df.isOpen == 0]['calendarDate'].values
        if isinstance(date, str):
            today = datetime.datetime.strptime(date, '%Y-%m-%d')

        if today.isoweekday() in [6, 7] or str(date) in holiday:
            return True
        else:
            return False

    @exc_time
    def trade_cal(self):

        sql = ("select * from trade_date")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def trade_truncate(self):

        sql = ("truncate table trade_date")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def init_pool(self):
        self.trade_truncate();
        df = ts.trade_cal()
        df.to_sql('trade_date', dataSource.mysql_quant_engine, if_exists='append', index=False)


trade_date_dao = Trade_Date_Dao()
