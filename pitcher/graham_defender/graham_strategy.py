# ae_h - 2018/7/18
import pandas as pd
import numpy as np
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.basic.stock_pool_dao import stock_pool_dao
from pitcher.strategy import Strategy
from common_tools.decorators import exc_time
from pitcher.context import Context
import tushare as ts


class GrahamDefender(Strategy):
    def init(self, context):
        super(GrahamDefender, self).init(context)

        # context.pool = stock_pool_dao.get_list()['code'].values
        self.context = context

    @exc_time
    def handle_data(self):
        stock_codes = list(stock_pool_dao.get_list()['code'].values)

        self.context.target_list = pd.DataFrame(columns=['code', 'pe', 'pb', 'eps', 'm_cap'])

        for code in stock_codes:
            stock_basic_info = stock_basic_dao.get_by_code(code=code)

            try:
                pe_value = stock_basic_info['pe'].values[0]
                pb_value = stock_basic_info['pb'].values[0]
                eps_value = stock_basic_info['eps'].values[0]
                m_cap = stock_basic_info['total_market'].values[0]
            except:
                pass

            if pe_value < 20 and pb_value < 1.8 and eps_value > 0:
                target_stock = {'code': code, 'pe': pe_value, 'pb': pb_value, 'eps': eps_value, 'm_cap': m_cap}
                self.context.target_list.loc[self.context.target_list.shape[0] + 1] = target_stock

        print(self.context.target_list.sort_values('m_cap', ascending=False)[:5])


if __name__ == '__main__':
    context = Context(start='2017-07-01', end='2018-07-14', base_capital=20000)
    graham_defender = GrahamDefender()
    graham_defender.init(context)
    graham_defender.handle_data()
    context.futu_quote_ctx.close()
