# ae_h - 2018/7/13

import pandas as pd


class Context:
    def __init__(self, start, end, base_capital):
        self.start = start
        self.end = end
        self.base_capital = base_capital
        self.profit_df = pd.DataFrame(
            columns=['stock_code', 'daily_profit', 'daily_change_rate', 'total_profit', 'total_change_rate'])
        self.order_book_df = pd.DataFrame(
            columns=['stock_code', 'action', 'shares', 'price_in', 'price_out', 'date_time'])
        self.protofolio_df = pd.DataFrame(
            columns=['stock_code', 'shares', 'price'])

    def __getattr__(self, item):
        return item
