import json
'''
    仓位类
'''
class Position(object):

    def __init__(self, code, price, shares, total, trade_fee , create_time):
        # 股票代码
        self.code = code
        # 价格
        self.price = price

        # 开仓均价
        self.price_in = price
        # 股数
        self.shares = shares

        # 总金额
        self.total = total

        # 交易费用
        self.trade_fee = trade_fee

        self.create_time = create_time


    @property
    def score(self):
        return self._score
