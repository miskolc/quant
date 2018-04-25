# ae.h - 2018/4/25

# Ultimate Oscillator

import pandas as pd
import tushare as ts

'''
 * 终极摆动指标
 * http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator
 
    # Close = data['close'].head(1).values[0]
    # Minimum = data['low'].values.min()
    #
    # Maximum = data['high'].values.max()
    #
    # BP = Close - Minimum
    # TR = Maximum - Minimum

 * BP = Close - Minimum(Low or Prior Close).

 * TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)

 * Average7 = (7-period BP Sum) / (7-period TR Sum)
 * Average14 = (14-period BP Sum) / (14-period TR Sum)
 * Average28 = (28-period BP Sum) / (28-period TR Sum)

 * UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

'''


def Ulto(data):
    # UO_V = pd.Series(100 * ((4 * av_7) + (2 * av_14) + av_28) / (4 + 2 + 1))
    # data = data.sort_index()

    BP = data['close'] - data['low']
    TR = data['high'] - data['low']

    av_7 = pd.rolling_sum(BP, 7) / pd.rolling_sum(TR, 7)
    av_14 = pd.rolling_sum(BP, 14) / pd.rolling_sum(TR, 14)
    av_28 = pd.rolling_sum(BP, 28) / pd.rolling_sum(TR, 28)

    ulto = 100 * ((4 * av_7) + (2 * av_14) + av_28) / (4 + 2 + 1)

    # Ulto = pd.Series(100 * ((4 * (pd.rolling_sum(BP, 7) / pd.rolling_sum(TR, 7))) + (
    #     2 * (pd.rolling_sum(BP, 14) / pd.rolling_sum(TR, 14))) + (pd.rolling_sum(BP, 28) / pd.rolling_sum(TR, 28)) / (
    #                      4 + 2 + 1)), name='ulto')
    return ulto
