# coding = utf-8
# ae.h - 2018/5/20
from talib import abstract
import pandas as pd
import numpy as np

'''
 * 顺势指标
 * CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)
 * Typical Price (TP) = (High + Low + Close)/3
 * Constant = .015
'''

def cal_cci(data, ndays):
    cci_func = abstract.Function('cci')
    cci = cci_func(data, ndays)
    return cci
