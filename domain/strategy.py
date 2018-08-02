"""
    策略
"""
from sqlalchemy import Column, String

from domain.base import Base


class Strategy(Base):
    # 股票代码
    code = Column(String, primary_key=True)
    # 策略code
    name = Column(String)
