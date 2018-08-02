
import copy

from common_tools.decorators import exc_time
from dao.data_source import dataSource
from domain.strategy import Strategy


class Strategy_Dao():

    @exc_time
    def query_all(self):
        with dataSource.session_ctx() as session:
            strategy_dbs = session.query(Strategy).all()

            return copy.deepcopy(strategy_dbs)


strategy_dao = Strategy_Dao()