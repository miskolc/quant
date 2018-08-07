from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from domain.base import Base

'''
    仓位类
'''
class Position(Base):

    # 股票代码
    code = Column(String, primary_key=True)
    # 策略code
    strategy_code = Column(String, primary_key=True)
    # 股票名称
    name = Column(String)
    # 当前价格
    price = Column(Float)
    # 成本价
    price_in = Column(Float)
    # 股数
    shares = Column(Integer)
    # 盈亏
    profit = Column(Float)
    # 市值
    worth = Column(Float)
    # 盈亏金额
    profit_value = Column(Float)

    '''
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

        self.create_time = create_time


'''