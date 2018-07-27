# ae_h - 2018/7/23

from pitcher.strategy import Strategy
from common_tools.decorators import exc_time

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

        