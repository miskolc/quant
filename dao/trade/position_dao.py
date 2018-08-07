import copy

from common_tools.decorators import exc_time
from dao.data_source import dataSource
from domain.position import Position


class Position_Dao():

    @exc_time
    def add(self, position):
        with dataSource.session_ctx() as session:
            session.add(position)

    @exc_time
    def update(self, position):
        with dataSource.session_ctx() as session:
            session.merge(position)

    @exc_time
    def delete(self, position):
        with dataSource.session_ctx() as session:
            session.delete(position)

    @exc_time
    def query_by_code(self, strategy_code, code):

        with dataSource.session_ctx() as session:
            position_dbs = session.query(Position).filter(Position.strategy_code == strategy_code , Position.code == code).one()

            return copy.deepcopy(position_dbs)

    @exc_time
    def query_by_strategy_code(self, strategy_code):

        with dataSource.session_ctx() as session:
            position_dbs = session.query(Position).filter(Position.strategy_code == strategy_code).all()

            return copy.deepcopy(position_dbs)

    @exc_time
    def query_all(self):

        with dataSource.session_ctx() as session:
            position_dbs = session.query(Position).all()

            return copy.deepcopy(position_dbs)

position_dao = Position_Dao()
