# ae.h - 2018/4/27

'''
william's R%

* %R = (Highest High - Close)/(Highest High - Lowest Low) * -100

* 当％R线达到80时，市场处于超卖状况，股价走势随时可能见底。因此，80的横线一般称为买进线，投资者在此可以伺机买入；相反，当％R线达到20时，市场处于超买状况，走势可能即将见顶，20的横线被称为卖出线。

* 当％R从超卖区向上爬升时，表示行情趋势可能转向，一般情况下，当％R突破50中轴线时，市场由弱市转为强市，是买进的讯号；相反，当％R从超买区向下跌落，跌破50中轴线后，可确认强市转弱，是卖出的讯号。

* 由于股市气势的变化，超买后还可再超买，超卖后亦可再超卖，因此，当％R进入超买或超卖区，行情并非一定立刻转势。只有确认％R线明显转向，跌破卖出线或突破买进线，方为正确的买卖讯号

* 在使用威廉指数对行情进行研制时，最好能够同时使用强弱指数配合验证。同时，当％R线突破或跌穿50中轴线时，亦可用以确认强弱指数的讯号是否正 确。因此，使用者如能正确应用威廉指数，发挥其与强弱指数在研制强弱市及超买超卖现象的互补功能，可得出对大势走向较明确的判断

(14日内最高价 - 当日收盘价)/(14日内最高价 - 14日内最低价) * -100

'''

import pandas as pd
import tushare as ts


def w_R_rate(data, ndays):
    highest_fourteen = pd.Series.rolling(data['high'], ndays).max()
    lowest_fourteen = pd.Series.rolling(data['low'], ndays).min()
    daily_close = pd.Series(data['close'])
    the_w_R_rate = pd.Series(abs((highest_fourteen - daily_close) / (highest_fourteen - lowest_fourteen) * -100), name='wr%s' %ndays)
    data = data.join(the_w_R_rate)

    return data

