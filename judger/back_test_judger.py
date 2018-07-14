# ae_h - 2018/7/12
from pitcher.context import Context
import matplotlib.pyplot as plt


class DailyBackTestJudger():
    def __init__(self, start, end, base_capital):
        self.context = Context(start, end, base_capital)
        return

    def execute(self, strategy):
        for date in self.get_trade_days():
            self.context.current_date = date
            strategy.handle_date(self.context)
        self.bt_plot()

    def get_trade_days(self):

        df = futu_get_trade_day()
        timeline_df = df[df['date'] == self.context.start: df['date'] == self.context.end]

        time_line = []
        for trade_day in timeline_df:
            time_line.append(trade_day)

        # [1-1, 1-2, 1-3, ..., 1-31]
        return time_line

    def bt_plot(self):
        self.context.base_profit = self.hs_300_base_profit()
        plt.plot(self.context.st_profit, label='strategy profit')
        plt.plot(self.context.base_profit, label='base profit')
        plt.show()

    def hs_300_base_profit(self):
        return k_data_dao.get_hs300_base_profit(start=self.context.start, end= self.context.end)