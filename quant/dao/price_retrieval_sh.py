# ae.h - 2018/4/23
from quant.dao import index_retrieval

if __name__ == '__main__':
    index_retrieval('000001', freq='1min', start_date='2015-01-01', end_date='2018-04-23')
