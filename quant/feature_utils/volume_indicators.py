# coding = utg-8
# ae.h - 2018/5/28
from talib import abstract
import pandas as pd
import numpy as np


def cal_ad(data):
    ad_func = abstract.Function('ad')
    ad = ad_func(data)
    return ad


def cal_adosc(data):
    adosc_func = abstract.Function('adosc')
    adosc = adosc_func(data)
    return adosc



def cal_obv(data):
    obv_func = abstract.Function('obv')
    obv = obv_func(data)
    return obv

