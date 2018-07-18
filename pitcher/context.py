# ae_h - 2018/7/13

import pandas as pd

from pitcher.domian.portfolio import Portfolio


class Context:
    def __init__(self, start, end, base_capital):
        # 开始时间
        self.start = start
        # 结束时间
        self.end = end
        # 总额
        self.base_capital = base_capital


        # 账户余额
        self.blance = base_capital

        self.profit_df = pd.DataFrame(
            columns=['code', 'daily_profit', 'daily_change_rate', 'total_profit', 'total_change_rate'])
        # 下单记录
        self.order_book = []
        # 投资组合, 'code', 'shares', 'price', 'total'
        self.portfolio = Portfolio()
        # 当前时间
        self.current_date = None

    def __getattr__(self, item):
        return item
