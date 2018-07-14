# ae_h - 2018/7/12
from dao import dataSource
from pitcher.context import Context
import matplotlib.pyplot as plt
from dao.k_data.k_data_dao import k_data_dao
from common_tools.decorators import exc_time
import pandas as pd
import numpy as np


class DailyBackTestJudger():
    def __init__(self, start, end, base_capital):
        self.context = Context(start, end, base_capital)
        return

    @exc_time
    def execute(self, strategy):
        for date in self.get_trade_days():
            self.context.current_date = date
            strategy.handle_date(self.context)
        self.bt_plot()

    @exc_time
    def get_trade_days(self):

        trade_days = list(k_data_dao.get_trading_days(start=self.context.start, end=self.context.end))
        # timeline_df = df[df['date'] == self.context.start: df['date'] == self.context.end]

        time_line = []
        for trade_day in trade_days:
            time_line.append(trade_day)

        # [1-1, 1-2, 1-3, ..., 1-31]
        return time_line

    @exc_time
    def bt_plot(self):
        self.context.base_profit = self.hs_300_base_profit()
        plt.plot(self.context.st_profit, label='strategy profit')
        plt.plot(self.context.base_profit, label='base profit')
        plt.show()

    @exc_time
    def hs_300_base_profit(self):
        hs_df = k_data_dao.get_k_data('SH.000300', start=self.context.start, end=self.context.end)

        self.context.hs_300_profit = pd.DataFrame(columns=['date', 'base_profit'])
        self.context.hs_300_profit['date'] = pd.to_datetime(hs_df['time_key'], format='%Y-%m-%d')
        for i in range(0, len(hs_df['change_rate'])):
            if i == 0:
                self.context.hs_300_profit['base_profit'].loc[i] = hs_df['change_rate'][i]
            else:
                self.context.hs_300_profit['base_profit'].loc[i] = hs_df['change_rate'].loc[:i].sum()
        print(self.context.hs_300_profit)



if __name__ == '__main__':
    dbt = DailyBackTestJudger(start='2018-01-02', end='2018-07-11', base_capital=50000)
    dbt.hs_300_base_profit()
    dataSource.futu_quote_ctx.close()
