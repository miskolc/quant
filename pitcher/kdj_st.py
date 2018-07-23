# ae_h - 2018/7/13
import traceback

import pandas as pd

from common_tools.datetime_utils import get_next_date
from common_tools.decorators import exc_time
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.basic.stock_pool_dao import stock_pool_dao
from dao.k_data.k_data_dao import k_data_dao
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from feature_utils.custome_features import cal_mavol5, cal_mavol20
from feature_utils.momentum_indicators import acc_kdj, cal_macd
from feature_utils.overlaps_studies import cal_ma5, cal_ma10, cal_ma20, cal_ma60
from log.quant_logging import logger
from pitcher.context import Context
from pitcher.strategy import Strategy
from dao.basic.stock_industry_dao import stock_industry_dao


class KDJStrategy(Strategy):
    def init(self, context):
        super(KDJStrategy, self).init(context)

        # context.pool = stock_pool_dao.get_list()['code'].values
        # context.pool = stock_industry_dao.get_list()['code'].values
        self.context = context
        context.pool = ['600198', '601398']

        # self.context.pool = ["000528"]

    def fill_zero(self, code):
        code = str(code)
        code = code.zfill(6)
        return code

    @exc_time
    def handle_data(self):
        target_frame = pd.DataFrame(columns=['code', 'close', 'k_value', 'd_value', 'pre_k', 'pre_d', 'macd',
                                             'pre_macd', 'diff', 'pre_diff', 'dea', 'pre_dea' 'current_vol_weekly',
                                             'pre_vol_weekly'])

        for code in self.context.pool:
            try:
                daily_stock_data = k_data_dao.get_k_data(code=code,
                                                         start=get_next_date(days=-100, args=context.current_date),
                                                         end=self.context.current_date,
                                                         futu_quote_ctx=self.futu_quote_ctx)
                weekly_stock_data = k_data_weekly_dao.get_k_data(code=code,
                                                                 start=None,
                                                                 end=None,
                                                                 futu_quote_ctx=self.futu_quote_ctx)

                pre_vol_weely = weekly_stock_data['volume'].iloc[-2:].values[0]
                current_vol_weekly = weekly_stock_data['volume'].iloc[-1:].values[0]
                daily_stock_data = daily_stock_data.join(acc_kdj(daily_stock_data))
                daily_stock_data_withf = daily_stock_data.join(cal_macd(daily_stock_data))

                k_value = daily_stock_data_withf['k_value'].iloc[-1:].values[0]
                d_value = daily_stock_data_withf['d_value'].iloc[-1:].values[0]
                pre_k = daily_stock_data_withf['k_value'].iloc[-2:].values[0]
                pre_d = daily_stock_data_withf['d_value'].iloc[-2:].values[0]
                pre_macd_value = daily_stock_data_withf['macd'].iloc[-2:].values[0]
                current_macd_value = daily_stock_data_withf['macd'].iloc[-1:].values[0]
                pre_macd_diff = daily_stock_data_withf['diff'].iloc[-2:].values[0]
                macd_diff = daily_stock_data_withf['diff'].iloc[-1:].values[0]
                pre_macd_dea = daily_stock_data_withf['dea'].iloc[-2:].values[0]
                macd_dea = daily_stock_data_withf['dea'].iloc[-2:].values[0]

                # 金叉
                # and current_macd_value >= current_macd_signal and pre_macd_value < current_macd_value and current_vol_weekly / pre_vol_weely >= 1.3
                # (k_value >= d_value or 10 >= abs(pre_k - pre_d) >= abs(k_value - d_value))
                if k_value >= d_value :
                    # and current_vol_weekly / pre_vol_weely >= 1.3 and (macd_diff > macd_dea)
                    # and abs(k_value - d_value) <= 5


                    # and current_macd_value >= current_macd_signal and pre_macd_value < current_macd_value \

                    # if k_value > d_value and abs(k_value - d_value) <= 20:
                    # basic_data = stock_basic_dao.get_by_code(code=code)
                    # 'bm': 1 / basic_data['pb'].loc[-1:].values[0],
                    last_close = daily_stock_data_withf['close'].iloc[-1:].values[0]
                    target_stock = {'code': self.fill_zero(code), 'close': last_close, 'k_value': k_value,
                                    'd_value': d_value, 'pre_k': pre_k, 'pre_d': pre_d,
                                    'macd': current_macd_value,
                                    'pre_macd': pre_macd_value, 'diff': macd_diff,
                                    'pre_diff': pre_macd_diff, 'dea': macd_dea, 'pre_dea': pre_macd_dea,
                                    'current_vol_weekly': current_vol_weekly, 'pre_vol_weekly': pre_vol_weely,
                                    }
                    target_frame.loc[target_frame.shape[0] + 1] = target_stock
                    print(target_stock)

                    # self.buy_in_percent(code=code, price=last_close, percent=0.1)
            except Exception as e:
                print(e)
                print(code)
                print(traceback.format_exc())
                continue
        target_frame.to_csv('kdj_result.csv')

        # 死叉
        # if pre_k > pre_d and ((k_value <= d_value) or (abs(k_value - d_value) <= 10)):
        #
        #     shares = self.context.portfolio.positions[code].shares
        #     # 清仓
        #     if shares > 0:
        #         self.sell_value(code, shares)


if __name__ == '__main__':
    context = Context(start='2018-07-01', end='2018-07-14', base_capital=50000)

    kdj = KDJStrategy()
    kdj.init(context)

    context.current_date = '2018-7-20'
    kdj.handle_data()

    logger.debug("base_capital:%s" % context.base_capital)
    logger.debug("blance:%s" % context.blance)

    # context.current_date = convert_to_datetime('2018-07-04')
    # kdj.handle_data()

    # logger.debug(context.order_book[1])
    logger.debug("blance:%s" % context.blance)
    logger.debug("base_capital:%s" % context.base_capital)

    kdj.futu_quote_ctx.close()
