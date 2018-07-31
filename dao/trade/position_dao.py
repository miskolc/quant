import copy

from common_tools.decorators import exc_time
from dao.data_source import dataSource
from domain.position import Position


def query_by_code(given_code):

    with dataSource.session_ctx() as session:
        position = session.query(Position).filter(Position.code == given_code).one()
        return position.to_dict()


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
    def query_by_strategy_code(self, given_code):

        with dataSource.session_ctx() as session:
            position_dbs = session.query(Position).filter(Position.strategy_code == given_code).all()
            rs = [position.to_dict() for position in position_dbs]

        return rs


position_dao = Position_Dao()
