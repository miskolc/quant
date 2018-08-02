
import copy

from common_tools.decorators import exc_time
from dao.data_source import dataSource
from domain.stock import Stock
from domain.strategy import Strategy


class Stock_Dao():

    @exc_time
    def query_by_code(self, code):
        with dataSource.session_ctx() as session:
            stock_dbs = session.query(Stock).filter(Stock.code == code).one()

            return copy.deepcopy(stock_dbs)


stock_dao = Stock_Dao()