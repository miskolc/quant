# ae_h - 2018/7/13

import json

import pandas as pd

from common_tools.datetime_utils import get_next_date
from common_tools.decorators import exc_time, error_handler
from common_tools.json_utils import obj_dict
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.basic.stock_pool_dao import stock_pool_dao
from dao.k_data.k_data_dao import k_data_dao
from feature_utils.custome_features import cal_mavol5, cal_mavol20
from feature_utils.momentum_indicators import acc_kdj
from feature_utils.overlaps_studies import cal_ma5, cal_ma10, cal_ma20, cal_ma60
from log.quant_logging import logger
from pitcher.context import Context
from pitcher.strategy import Strategy


class KDJStrategy(Strategy):
    def init(self, context):
        super(KDJStrategy, self).init(context)

        context.pool = stock_pool_dao.get_list()['code'].values
        self.context = context
        # self.context.pool = ["000528","002008","600256","600536","600801"]

    def fill_zero(self, code):
        code = str(code)
        code = code.zfill(6)
        return code

    @exc_time
    def handle_data(self):
        target_frame = pd.DataFrame(
            columns=['code', 'close', 'k_value', 'd_value', 'pre_k', 'pre_d', 'ma20', 'profits_yoy', 'bm', 'mavol5',
                     'mavol20'])
        for code in self.context.pool:

            daily_stock_data = self.get_k_data(code=code,
                                                     start=get_next_date(days=-30, args=self.context.current_date),
                                                     end=self.context.current_date)

            daily_stock_data = daily_stock_data.join(acc_kdj(daily_stock_data))

            k_value = daily_stock_data['k_value'].iloc[-1:].values[0]
            d_value = daily_stock_data['d_value'].iloc[-1:].values[0]
            pre_k = daily_stock_data['k_value'].iloc[-2:].values[0]
            pre_d = daily_stock_data['d_value'].iloc[-2:].values[0]

            # 金叉
            if (k_value >= d_value or abs(k_value - d_value) <= 10) and pre_k <= pre_d:

                feature_frame = pd.concat(
                    [acc_kdj(daily_stock_data), cal_ma5(daily_stock_data), cal_ma10(daily_stock_data),
                     cal_ma20(daily_stock_data), cal_ma60(daily_stock_data), cal_mavol5(daily_stock_data),
                     cal_mavol20(daily_stock_data)], axis=1)

                feature_frame.columns = ['k_value', 'd_value', 'j_value', 'ma5', 'ma10', 'ma20', 'ma60', 'mavol5',
                                         'mavol20']
                # weekly_stock_date = k_data_weekly_dao.get_k_data(code=code,start=get_next_date(days=-300,
                # args=context.current_date),end=get_current_date(context.current_date)) weekly_stock_date =
                # weekly_stock_date.join(acc_kdj(weekly_stock_date))
                basic_data = self.get_stock_basic(code=code)
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
                # and mavol5 > mavol20
                if last_close > ma5_close and profits_yoy > 30:
                    target_stock = {'code': self.fill_zero(code), 'close': last_close, 'k_value': k_value,
                                    'd_value': d_value, 'pre_k': pre_k, 'pre_d': pre_d,
                                    'ma20': ma20_close, 'profits_yoy': profits_yoy,
                                    'bm': 1 / basic_data['pb'].loc[-1:].values[0], 'mavol5': mavol5, 'mavol20': mavol20}
                    target_frame.loc[target_frame.shape[0] + 1] = target_stock

                    self.buy_in_percent(code=code, price=last_close, percent=0.2)



            # target_frame.to_csv('kdj_result.csv')
            # 死叉
            if pre_k > pre_d and (k_value <= d_value):

                 position = self.context.portfolio.get_position(code)

                 # 清仓
                 if position is not None and position.shares > 0:
                     self.sell_value(code, position.shares)


@error_handler()
def back_test():
    context = Context(start='2017-01-01', end='2018-07-14', base_capital=50000)

    kdj = KDJStrategy()
    kdj.init(context)

    try:

        trade_days = list(
            k_data_dao.get_trading_days(start=context.start, end=context.end, futu_quote_ctx=kdj.futu_quote_ctx))

        kdj.before_trade()

        for date in trade_days:

            context.current_date = date
            kdj.before_handle_data()

            kdj.handle_data()

    finally:
        kdj.futu_quote_ctx.close()

    context_json = json.dumps(context, default=obj_dict)
    logger.debug("context:" + context_json)

if __name__ == '__main__':
    back_test()