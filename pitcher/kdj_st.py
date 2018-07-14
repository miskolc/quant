# ae_h - 2018/7/13
import datetime

import numpy as np
from dao.k_data.k_data_dao import k_data_dao
from common_tools.decorators import exc_time
from feature_utils.momentum_indicators import acc_kdj
from pitcher.context import Context
from dao.data_source import dataSource
from common_tools.datetime_utils import get_current_date, get_next_date


class KDJStrategy:
    @exc_time
    def handle_data(self, context):
        stock_data = k_data_dao.get_k_data(code='SZ.000528', start=get_next_date(days=-30, args=context.current_date), end=get_current_date(context.current_date))

        stock_data = stock_data.join(acc_kdj(stock_data))

        k_value = stock_data['k_value'].iloc[-1:].values[0]
        d_value = stock_data['d_value'].iloc[-1:].values[0]
        pre_k = stock_data['k_value'].iloc[-2:].values[0]
        pre_d = stock_data['d_value'].iloc[-2:].values[0]
        print((k_value, d_value), (pre_k, pre_d))



if __name__ == '__main__':

    context = Context(start='2018-07-01', end='2018-07-14', base_capital=50000)
    context.current_date = datetime.datetime.now()
    kdj = KDJStrategy()
    kdj.handle_data(context)
    dataSource.futu_quote_ctx.close()
