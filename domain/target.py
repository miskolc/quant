from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from domain.base import Base

'''
    预选股
'''


class Target(Base):
    # 股票代码
    code = Column(String, primary_key=True)
    # 策略code
    strategy_code = Column(String, primary_key=True)
    # 股票名称
    name = Column(String)
    # 价格
    price = Column(Float)
    # 买入点
    pointcut = Column(Float)