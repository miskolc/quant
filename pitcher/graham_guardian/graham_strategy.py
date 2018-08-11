# ae_h - 2018/7/18
import json
from datetime import datetime

import pandas as pd
import numpy as np

from common_tools.datetime_utils import get_next_date
from common_tools.json_utils import obj_dict
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.basic.stock_pool_dao import stock_pool_dao
from dao.k_data.k_data_dao import k_data_dao
from log.quant_logging import logger
from pitcher.strategy import Strategy
from common_tools.decorators import exc_time
from pitcher.context import Context
import datetime as dt
import tushare as ts


class GrahamDefender(object):
    def init(self, context):
        # super(GrahamDefender, self).init(context)

        # context.pool = list(stock_pool_dao.get_list()['code'].values)
        context.pool = list(stock_pool_dao.get_list()['code'].values)

        self.context = context

    @exc_time
    def handle_data(self):

        temp_target_list = pd.DataFrame(columns=['code', 'pe', 'pb', 'eps', 'm_cap'])

        sh_index = k_data_dao.get_k_data('SH.000001', start=get_next_date(-30), end=get_next_date(-1))

        # if sh_index['change_rate'].rolling(window=3).sum().values[-1] >= -0.039:
        #     for position in context.portfolio.positions[:]:
        #         code = position.code
        #         shares = position.shares
        #         price = position.price
        #         self.sell_value(code=code, shares=shares, price=price)

        for code in self.context.pool:
            stock_basic_info = stock_basic_dao.get_by_code(code=code)
            if len(stock_basic_info) == 0:
                continue

            try:
                pe_value = stock_basic_info['pe'].values[0]
                pb_value = stock_basic_info['pb'].values[0]
                eps_value = stock_basic_info['eps'].values[0]
                m_cap = stock_basic_info['total_market'].values[0]
            except:
                pass

            if pe_value < 20 and pb_value < 1.8 and eps_value > 0:
                target_stock = {'code': code, 'pe': pe_value, 'pb': pb_value, 'eps': eps_value, 'm_cap': m_cap}
                temp_target_list.loc[temp_target_list.shape[0] + 1] = target_stock

        temp_target_stock = temp_target_list.sort_values('m_cap', ascending=False)[:5]
        target_code_list = temp_target_stock['code'].values

        current_stock_code = []
        for positions in self.context.portfolio.positions:
            current_stock_code.append(positions.code)
        print(current_stock_code)

        stock_to_be_added = [i for i in target_code_list if i not in current_stock_code]
        stock_to_be_removed = [j for j in current_stock_code if j not in target_code_list]

        for code in stock_to_be_removed:

            # self.sell_value(code=code, price=price, shares=-1)

            logger.info('direction = sell:' + code)

        for code in stock_to_be_added:
            #k_data = k_data_dao.get_k_data(code=code, start=self.context.current_date, end=self.context.current_date)

            #if len(k_data) == 0:
                #continue

            #price = k_data['close'].values[-1]

            #if len(self.context.portfolio.positions) >= 5:
                #break
            # self.buy_in_percent(code=code, price=price, percent=0.2)
            k_data = k_data_dao.get_k_data(code=code, start=get_next_date(-2), end=self.context.current_date)
            price = k_data['close'].values[-1]
            shares = int(4000 / price / 100) * 100

            print('direction = buy:%s, shares:%s'%(code, shares))
        #self.context.next_open = datetime.strptime(self.context.current_date, '%Y-%m-%d') + dt.timedelta(days=20)


if __name__ == '__main__':
    graham_defender = GrahamDefender()
    try:
        context = Context(start='2017-07-01', end='2018-07-29', base_capital=20000)

        graham_defender.init(context)

        context.current_date = '2018-07-29'

        graham_defender.handle_data()

        # context.current_date = '2018-01-22'
        # graham_guardian.before_handle_data()
        # graham_guardian.handle_data()
        #context_json = json.dumps(context, default=obj_dict)

        #logger.debug("context:" + context_json)
        # graham_guardian.futu_quote_ctx.close()
    finally:
        # graham_guardian.futu_quote_ctx.close()
        pass
