from dao.trade.stock_dao import stock_dao
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException


class StockHandler(BaseHandler):

    """
        Handle for endpoint: /stock/{code}
    """

    def on_get(self, req, resp, code):
        stock_dbs = stock_dao.query_by_code(code)

        if stock_dbs is None:
            raise ResourceNotFoundException("Can not found stock.")

        self.on_success(resp=resp, data=stock_dbs)
