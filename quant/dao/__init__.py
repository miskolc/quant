# greg.chen - 2018/5/19

from quant.dao.data_source import dataSource

def cal_direction(x):
    if x > 0:
        return 1
    elif x is None:
        return None
    else:
        return 0



