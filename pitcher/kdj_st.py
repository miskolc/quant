# ae_h - 2018/7/13
import datetime

import pandas as pd

from common_tools.datetime_utils import get_current_date, get_next_date
from common_tools.decorators import exc_time
from config import default_config
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.k_data.k_data_dao import k_data_dao
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from feature_utils.momentum_indicators import acc_kdj
from feature_utils.custome_features import cal_mavol5, cal_mavol20
from feature_utils.overlaps_studies import cal_ma5, cal_ma10, cal_ma20, cal_ma60
from pitcher.context import Context
from dao.basic.stock_pool_dao import stock_pool_dao
import futuquant as ft


class KDJStrategy:
    def init(self, context):
        context.pool = stock_pool_dao.get_list()['code'].values
        context.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                     port=default_config.FUTU_OPEND_PORT)

    def fill_zero(self, code):
        code = str(code)
        code = code.zfill(6)
        return code

    # def buy_in(self, stock):
        # context.buy_in_price =

    @exc_time
    def handle_data(self, context):
        target_frame = pd.DataFrame(
            columns=['code', 'close', 'k_value', 'd_value', 'pre_k', 'pre_d', 'ma20', 'profits_yoy', 'bm', 'mavol5',
                     'mavol20'])
        for code in context.pool:
            daily_stock_data = k_data_dao.get_k_data(code=code,
                                                     start=get_next_date(days=-30, args=context.current_date),
                                                     end=get_current_date(context.current_date),
                                                     futu_quote_ctx=context.futu_quote_ctx)

            daily_stock_data = daily_stock_data.join(acc_kdj(daily_stock_data))
            try:
                k_value = daily_stock_data['k_value'].iloc[-1:].values[0]
                d_value = daily_stock_data['d_value'].iloc[-1:].values[0]
                pre_k = daily_stock_data['k_value'].iloc[-2:].values[0]
                pre_d = daily_stock_data['d_value'].iloc[-2:].values[0]
            except:
                continue
            # 金叉
            if (k_value >= d_value or abs(k_value - d_value) <= 10) and abs(k_value - d_value) < abs(
                            pre_k - pre_d) and pre_k <= pre_d:

                feature_frame = pd.concat(
                    [acc_kdj(daily_stock_data), cal_ma5(daily_stock_data), cal_ma10(daily_stock_data),
                     cal_ma20(daily_stock_data), cal_ma60(daily_stock_data), cal_mavol5(daily_stock_data),
                     cal_mavol20(daily_stock_data)], axis=1)

                feature_frame.columns = ['k_value', 'd_value', 'j_value', 'ma5', 'ma10', 'ma20', 'ma60', 'mavol5',
                                         'mavol20']
                # weekly_stock_date = k_data_weekly_dao.get_k_data(code=code,start=get_next_date(days=-300,
                # args=context.current_date),end=get_current_date(context.current_date)) weekly_stock_date =
                # weekly_stock_date.join(acc_kdj(weekly_stock_date))
                basic_data = stock_basic_dao.get_by_code(code=code)
                last_close = daily_stock_data['close'].iloc[-1:].values[0]
                ma5_close = feature_frame['ma5'].iloc[-1:].values[0]
                ma10_close = feature_frame['ma10'].iloc[-1:].values[0]
                ma20_close = feature_frame['ma20'].iloc[-1:].values[0]
                profits_yoy = basic_data['profits_yoy'].iloc[0]
                mavol5 = feature_frame['mavol5'].iloc[-1:].values[0]
                mavol20 = feature_frame['mavol20'].iloc[-1:].values[0]
                # w_k_value = weekly_stock_date['k_value'] = weekly_stock_date['k_value'].iloc[-1:].values[0]
                # w_d_value = weekly_stock_date['d_value'] = weekly_stock_date['d_value'].iloc[-1:].values[0]
                # pre_w_k_value = weekly_stock_date['k_value'] = weekly_stock_date['k_value'].iloc[-2:].values[0]
                # pre_w_d_value = weekly_stock_date['d_value'] = weekly_stock_date['d_value'].iloc[-2:].values[0]
                #
                if last_close > ma5_close and profits_yoy > 30:
                    target_stock = {'code': self.fill_zero(code), 'close': last_close, 'k_value': k_value,
                                    'd_value': d_value, 'pre_k': pre_k, 'pre_d': pre_d,
                                    'ma20': ma20_close, 'profits_yoy': profits_yoy,
                                    'bm': 1 / basic_data['pb'].loc[-1:].values[0], 'mavol5': mavol5, 'mavol20': mavol20}
                    target_frame.loc[target_frame.shape[0] + 1] = target_stock


        target_frame.to_csv('kdj_result.csv')
        # 死叉
        #     if pre_k > pre_d and ((k_value <= d_value) or (abs(k_value - d_value)<=10)):


if __name__ == '__main__':
    context = Context(start='2018-07-01', end='2018-07-14', base_capital=50000)
    context.current_date = datetime.datetime.now()
    kdj = KDJStrategy()
    kdj.init(context)
    kdj.handle_data(context)
    context.futu_quote_ctx.close()
