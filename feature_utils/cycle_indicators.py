# coding = utf-8
# ae.h - 2018/5/28

from talib import abstract
import pandas as pd
import numpy as np


def cal_ht_dcperiod(data):
    ht_dcperiod_func = abstract.Function('ht_dcperiod')
    ht_dcperiod = ht_dcperiod_func(data)
    return ht_dcperiod


def cal_ht_dcphase(data):
    ht_dcphase_func = abstract.Function('ht_dcphase')
    ht_dcphase = ht_dcphase_func(data)
    return ht_dcphase


def cal_ht_phasor(data):
    ht_phasor_func = abstract.Function('ht_phasor')
    ht_phasor = ht_phasor_func(data)
    return ht_phasor


def cal_ht_sine(data):
    ht_sine_func = abstract.Function('ht_sine')
    ht_sine = ht_sine_func(data)
    return ht_sine


def cal_ht_trendmode(data):
    ht_trendmode_func = abstract.Function('ht_trendmode')
    ht_trendmode = ht_trendmode_func(data)
    return ht_trendmode
