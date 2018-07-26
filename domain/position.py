from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from domain import Base

'''
    仓位类
'''
class Position(Base):
    __tablename__ = 'position'
    code = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    price_in = Column(Float)
    shares = Column(Integer)
    create_time = Column(DateTime)

    def __init__(self, code, name, price, price_in, shares):
        self.code = code
        self.name = name
        self.price = price
        self.price_in = price_in
        self.shares = shares

    @hybrid_property
    def total_market(self):
        return round(self.price * self.shares,2)

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