from common_tools.decorators import exc_time

from dao.data_source import dataSource
from domain.position import Position
from dao.orm_serializer import serielizer


class Position_Dao():
    @exc_time
    def get_position_list(self):
        rs = []
        with dataSource.session_ctx() as session:
            for row in session.query(Position).all():
                position = Position(code=row.code, name=row.name, price=row.price, price_in=row.price_in,
                                    shares=row.shares)

                # position["code"]=row.code

                rs.append(position)

        return rs

    def update(self, position):
        with dataSource.session_ctx() as session:
            session.merge(position)

    def delete(self, position):
        with dataSource.session_ctx() as session:
            session.delete(position)

    def query_by_code(self, given_code):

        with dataSource.session_ctx() as session:
            for instance in session.query(Position).filter(Position.code == given_code).all():
                print(serielizer(instance))




position_dao = Position_Dao()
