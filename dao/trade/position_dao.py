from common_tools.decorators import exc_time

from dao.data_source import dataSource
from observer.domain.position import Position


class Position_Dao():
    @exc_time
    def get_position_list(self):

        rs = []
        with dataSource.session_ctx() as session:
            for row in session.query(Position).all():
                position = Position(code=row.code, name=row.name, price=row.price, price_in=row.price_in, shares = row.shares)

                #position["code"]=row.code

                rs.append(position)

        return rs

    def update(self, position):
        with dataSource.session_ctx() as session:
            session.merge(position)


position_dao = Position_Dao()

