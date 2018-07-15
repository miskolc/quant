# ae_h - 2018/7/13
import datetime

import pandas as pd

from common_tools.datetime_utils import get_current_date, get_next_date
from common_tools.decorators import exc_time
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.k_data.k_data_dao import k_data_dao
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from feature_utils.custome_features import cal_mavol5, cal_mavol10, cal_mavol20
from feature_utils.momentum_indicators import acc_kdj
from feature_utils.overlaps_studies import cal_ma5, cal_ma10, cal_ma20, cal_ma60
from pitcher.context import Context
from dao.basic.stock_pool_dao import stock_pool_dao


class KDJStrategy:

    def init(self, context):
        context.pool = stock_pool_dao.get_list()['code'].values

    @exc_time
    def handle_data(self, context):
        # for code in context.pool:
        target_list = []
        for code in context.pool:
            daily_stock_data = k_data_dao.get_k_data(code=code, start=get_next_date(days=-30, args=context.current_date),
                                               end=get_current_date(context.current_date))

            daily_stock_data = daily_stock_data.join(acc_kdj(daily_stock_data))
            try:
                k_value = daily_stock_data['k_value'].iloc[-1:].values[0]
                d_value = daily_stock_data['d_value'].iloc[-1:].values[0]
                pre_k = daily_stock_data['k_value'].iloc[-2:].values[0]
                pre_d = daily_stock_data['d_value'].iloc[-2:].values[0]
            except:
                continue

            # 金叉
            if pre_k < pre_d and ((k_value >= d_value) or (abs(k_value - d_value)<=5)):
                feature_frame = pd.concat([acc_kdj(daily_stock_data), cal_ma5(daily_stock_data), cal_ma10(daily_stock_data),
                                           cal_ma20(daily_stock_data), cal_ma60(daily_stock_data)], axis=1)

                feature_frame.columns = ['k_value', 'd_value', 'j_value', 'ma5', 'ma10', 'ma20', 'ma60']
                weekly_stock_date = k_data_weekly_dao.get_k_data(code=code,
                                                                 start=get_next_date(days=-300, args=context.current_date),
                                                                 end=get_current_date(context.current_date))
                # weekly_stock_date = weekly_stock_date.join(acc_kdj(weekly_stock_date))
                basic_data = stock_basic_dao.get_by_code(code=code[3:])
                # w_k_value = weekly_stock_date['k_value'] = weekly_stock_date['k_value'].iloc[-1:].values[0]
                # w_d_value = weekly_stock_date['d_value'] = weekly_stock_date['d_value'].iloc[-1:].values[0]
                # pre_w_k_value = weekly_stock_date['k_value'] = weekly_stock_date['k_value'].iloc[-2:].values[0]
                # pre_w_d_value = weekly_stock_date['d_value'] = weekly_stock_date['d_value'].iloc[-2:].values[0]

                if daily_stock_data['close'].iloc[-1:].values[0] > feature_frame['ma20'].iloc[-1:].values[0] and (basic_data['profits_yoy'].iloc[0] > -7):
                    target_list.append(code)
        print(target_list)


        # 死叉
        # if pre_k > pre_d and ((k_value <= d_value) or (abs(k_value - d_value)<=5)):




if __name__ == '__main__':
    context = Context(start='2018-07-01', end='2018-07-14', base_capital=50000)
    context.current_date = datetime.datetime.now()
    kdj = KDJStrategy()
    kdj.init(context)
    kdj.handle_data(context)

