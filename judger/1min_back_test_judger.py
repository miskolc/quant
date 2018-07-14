# ae_h - 2018/7/12
from pitcher.context import Context
import matplotlib.pyplot as plt


class DailyBackTestJudger():
    def __init__(self, start, end, base_capital):
        self.context = Context(start, end, base_capital)
        return

    def execute(self, st):


        for date in self.get_trade_days():
            self.context.current_date = date
            st(self.context)

        #self.bt_plot()

    def get_trade_days(self):

        # self.context.start, self.context.end

        return ['2017-01-01','2017-01-02','2017-01-03']


    def bt_plot(self):
        plt.plot(self.context.st_profit)
        plt.plot(self.context.base_profit)
        plt.show()
