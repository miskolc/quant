# ae.h - 2018/4/25

# Ultimate Oscillator

'''
 * 终极摆动指标
 * http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator

 * BP = Close - Minimum(Low or Prior Close).

 * TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)

 * Average7 = (7-period BP Sum) / (7-period TR Sum)
 * Average14 = (14-period BP Sum) / (14-period TR Sum)
 * Average28 = (28-period BP Sum) / (28-period TR Sum)

 * UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)


    # Close = data['close'].head(1).values[0]
    # Minimum = data['low'].values.min()
    #
    # Maximum = data['high'].values.max()
    #
    # BP = Close - Minimum
    # TR = Maximum - Minimum

'''


def UO(data):
    av_7 = get_x_period_av(data, 7)
    av_14 = get_x_period_av(data, 14)
    av_28 = get_x_period_av(data, 28)

    UO_value = 100 * ((4 * av_7) + (2 * av_14) + av_28) / (4 + 2 + 1)
    return UO_value


def get_x_period_av(data, x):
    return sum(data['close'][:x].values - data['low'][:x].values) / sum(
        data['high'][:x].values - data['low'][:x].values)
