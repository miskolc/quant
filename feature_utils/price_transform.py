# coding=utf-8
# ae.h - 2018/5/28

from talib import abstract
import pandas as pd
import numpy as np


def cal_avgprice(data):
    avgprice_func = abstract.Function('avgprice')
    avgprice = avgprice_func(data)
    return avgprice

def cal_medprice(data):
    medprice_func = abstract.Function('medprice')
    medprice = medprice_func(data)
    return medprice

def cal_typprice(data):
    typprice_func = abstract.Function('typprice')
    typprice = typprice_func(data)
    return typprice


def cal_wclprice(data):
    wclprice_func = abstract.Function('wclprice')
    wclprice = wclprice_func(data)
    return wclprice
