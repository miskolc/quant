# ae_h - 2018/7/23
from pitcher.context import Context
from pitcher.strategy import Strategy
from common_tools.decorators import exc_time
from dao.k_data.k_data_dao import k_data_dao
from feature_utils.overlaps_studies import cal_ma20, cal_ma145, cal_ma250
import pandas as pd


class HitAndRunStrategy(Strategy):
    def init(self, context):
        super(HitAndRunStrategy, self).init(context)

        # context.pool = stock_pool_dao.get_list()['code'].values
        self.context = context

    @exc_time
    def handle_data(self):
        '''
        1st_touch: ma250*.97<=low<=ma250, close>=ma250, can repeat until trend turn;
        if trend up:
            if touch ma145(close>=ma145): buy in
        elif trend up and close <= ma145: observe (til touch)
            elif trend turn: sell
        else trend turn down:
        wait for 2nd_touch: ma250*.3<=low<=ma250, close>=ma250:
        if trend keep up:
            1st buy
            if touch ma145:
                2nd buy
                trend keep: hold
                trend turn: sell
        else trend turn down:
            sell
        '''

        df = k_data_dao.get_k_data(code='603799', start='2016-07-01', end='2018-07-27')
        df['ma20'] = cal_ma20(df)
        df['ma145'] = cal_ma145(df)
        df['ma250'] = cal_ma250(df)
        print(df)


if __name__ == '__main__':
    context = Context(start='2016-07-01', end='2018-07-27', base_capital=50000)
    hnr = HitAndRunStrategy()
    hnr.handle_data()
