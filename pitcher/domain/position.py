import json
'''
    仓位类
'''
class Position(object):

    def __init__(self, code, price, shares, total, create_time):
        # 股票代码
        self.code = code
        # 价格
        self.price = price
        # 股数
        self.shares = shares
        # 总金额
        self.total = total

        self.create_time = create_time


    def __repr__(self):

        return json.dumps(self.__dict__)
