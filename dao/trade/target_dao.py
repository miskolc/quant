
import copy

from common_tools.decorators import exc_time
from dao.data_source import dataSource
from domain.target import Target


class Target_Dao():

    @exc_time
    def query_all(self):
        with dataSource.session_ctx() as session:
            strategy_dbs = session.query(Target).all()

            return copy.deepcopy(strategy_dbs)


    @exc_time
    def add(self, target):
        with dataSource.session_ctx() as session:
            session.add(target)

    @exc_time
    def update(self, target):
        with dataSource.session_ctx() as session:
            session.merge(target)

    @exc_time
    def delete(self, target):
        with dataSource.session_ctx() as session:
            session.delete(target)


    @exc_time
    def query_by_id(self, id):

        with dataSource.session_ctx() as session:
            position_dbs = session.query(Target).filter(Target.id == id).one()

            return copy.deepcopy(position_dbs)

target_dao = Target_Dao()