'''
    投资组合类
'''
from copy import deepcopy

from pitcher.domain.position import Position


class Portfolio:
    def __init__(self):
        # 仓位列表
        self.__positions = []
        self.position_history = []

    @property
    def positions(self):

        if len(self.__positions) > 0:
            return []

        return self.__positions[:]



    # 通过code, 获取仓位
    def get_position(self, code):

        for position in self.__positions:
            if position.code == code:
                return position

        return None

    def delete_position(self, code):
        for position in self.__positions:
            if position.code == code:
                self.__positions.remove(position)
                return

    def add_position(self, code, price, shares, total, trade_fee, date):

        position = self.get_position(code)

        if position is not None:
            position.price += price
            position.shares += shares
            position.total += total
            position.trade_fee += trade_fee

        else:
            # 新增投资组合
            position = Position(code, price, shares, total, trade_fee, date)
            # 记录投资组合
            self.__positions.append(position)

