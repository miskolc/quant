# ae_h - 2018/7/13

import pandas as pd


class Context:
    def __init__(self, start, end, base_capital):
        self.start = start
        self.end = end
        self.base_capital = base_capital
        self.profit_df = pd.DataFrame(columns=[ ])
        self.protofolio_df = pd.DataFrame(columns=[??])
        self.order_book_df = pd.DataFrame(columns=[??])


    def __getattr__(self, item):
        return item
