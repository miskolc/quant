# ae.h - 2018/4/23
from dao.price_retrieval import index_retrieval
import tushare as ts
import numpy as np

if __name__ == '__main__':
    index_retrieval('000001', freq='1min', start_date='2015-01-01', end_date='2018-04-23')
