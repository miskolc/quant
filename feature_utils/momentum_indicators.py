# coding = utf-8
# ae.h - 2018/5/20
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from talib import abstract
import pandas as pd
from feature_utils.f_utils import acc_SMA


def cal_adx(data):
    adx_func = abstract.Function('adx')
    adx = adx_func(data)
    return adx


def cal_adxr(data):
    adxr_func = abstract.Function('adxr')
    adxr = adxr_func(data)
    return adxr


def cal_apo(data):
    apo_func = abstract.Function('apo')
    apo = apo_func(data)
    return apo


def cal_aroon(data):
    aroon_func = abstract.Function('aroon')
    aroon = aroon_func(data)
    return aroon


def cal_aroonosc(data):
    aroonosc_func = abstract.Function('aroonosc')
    aroonosc = aroonosc_func(data)
    return aroonosc


def cal_bop(data):
    bop_func = abstract.Function('bop')
    bop = bop_func(data)
    return bop


def cal_cci(data, period=14):
    cci_func = abstract.Function('cci')
    cci = cci_func(data, timeperio=period)
    return cci


def cal_cmo(data):
    cmo_func = abstract.Function('cmo')
    cmo = cmo_func(data)
    return cmo


def cal_dx(data):
    dx_func = abstract.Function('dx')
    dx = dx_func(data)
    return dx


def cal_macd(data):
    macd_func = abstract.Function('macd')
    macd = macd_func(data)
    return macd


def cal_mfi(data):
    mfi_func = abstract.Function('mfi')
    mfi = mfi_func(data)
    return mfi


def cal_minus_di(data):
    minus_di_func = abstract.Function('minus_di')
    minus_di = minus_di_func(data)
    return minus_di


def cal_minus_dm(data):
    minus_dm_func = abstract.Function('minus_dm')
    minus_dm = minus_dm_func(data)
    return minus_dm


def cal_mom(data):
    mom_func = abstract.Function('mom')
    mom = mom_func(data)
    return mom


def cal_ppo(data):
    ppo_func = abstract.Function('ppo')
    ppo = ppo_func(data)
    return ppo


def cal_roc(data):
    roc_func = abstract.Function('roc')
    roc = roc_func(data)
    return roc


def cal_rsi(data):
    rsi_func = abstract.Function('rsi')
    rsi = rsi_func(data)
    return rsi


# def cal_stoch(data):
#     stoch_func = abstract.Function('stoch')
#     stoch = stoch_func(data, fastk_period=9, slowk_period=3, slowd_period=3, slowk_matype=1)
#     print(stoch)
#     return stoch
#
# def cal_stochf(data):
#     stochf_func = abstract.Function('stochf')
#     stochf = stochf_func(data)
#     print(stochf)
#     return stochf


def cal_ultosc(data):
    ultosc_func = abstract.Function('ultosc')
    ultosc = ultosc_func(data)
    return ultosc


def cal_willr_10(data):
    willr_10_func = abstract.Function('willr')
    willr_10 = willr_10_func(data, timeperiod=10)
    return willr_10


def cal_willr_14(data):
    willr_14_func = abstract.Function('willr')
    willr_14 = willr_14_func(data, timeperiod=14)
    return willr_14


def cal_willr_28(data):
    willr_28_func = abstract.Function('willr')
    willr_28 = willr_28_func(data, timeperiod=28)
    return willr_28


def acc_kdj(data, N1=9, N2=3, N3=3):
    low1 = pd.Series.rolling(data.low, N1).min()
    high1 = pd.Series.rolling(data.high, N1).max()
    rsv = (data.close - low1) / (high1 - low1) * 100
    k = acc_SMA(rsv, N2)
    d = acc_SMA(k, N3)
    j = k * 3 - d * 2
    kdj_df = pd.DataFrame(columns=['k_value', 'd_value', 'j_value'])
    kdj_df['k_value'] = k
    kdj_df['d_value'] = d
    kdj_df['j_value'] = j

    return kdj_df
