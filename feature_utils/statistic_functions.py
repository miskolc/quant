# ae_h - 2018/6/12

from talib import abstract


def cal_beta(data):
    beta_func = abstract.Function('beta')
    beta = beta_func(data)
    return beta
