import pandas as pd

# Compute the Bollinger Bands
'''

  * Middle Band = 20-day simple moving average (SMA)
  * Upper Band = 20-day SMA + (20-day standard deviation of price x 2) 
  * Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
  
  link: http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:bollinger_bands
'''


def sh_index_daily(start, end):

    MA = pd.Series(pd.Series.rolling(data['close'], ndays).mean())
    # SD 标准偏差
    SD = pd.Series(pd.Series.rolling(data['close'], ndays).std())

    b1 = MA + (2 * SD)
    B1 = pd.Series(b1, name='ubb')
    data = data.join(B1)

    b2 = MA - (2 * SD)
    B2 = pd.Series(b2, name='lbb')
    data = data.join(B2)

    return data
