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

