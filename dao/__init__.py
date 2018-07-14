# greg.chen - 2018/5/19

from dao.data_source import dataSource

def cal_direction(x, i=0):
    if x > i:
        return 1
    elif x is None:
        return None
    else:
        return 0



