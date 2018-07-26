'''
    投资组合类
'''


class Portfolio:
    def __init__(self):
        # 仓位列表
        self.positions = []
        self.position_history = []

    # 通过code, 获取仓位
    def get_position(self, code):

        for position in self.positions:
            if position.code == code:
                return position

        return None

    def delete_position(self, code):
        for position in self.positions:
            if position.code == code:
                self.positions.remove(position)
                return
