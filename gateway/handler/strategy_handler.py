from dao.trade.strategy_dao import strategy_dao
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException


class StrategySearchHandler(BaseHandler):

    """
        Handle for endpoint: /strategy/search
    """

    def on_post(self, req, resp):

        strategy_dbs = strategy_dao.query_all()

        if strategy_dbs is None:
            raise ResourceNotFoundException("Can not found position list.")

        self.on_success(resp=resp, data=strategy_dbs)
