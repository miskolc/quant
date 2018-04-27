from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.CCI import CCI
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.pre_close as pre_close
import app.custom_feature_calculating.index_sh as index_sh
import app.custom_feature_calculating.K_w_R_rate as w_R_rate
from app.custom_feature_calculating.FI import ForceIndex
import app.custom_feature_calculating.MACD as macd
from app.custom_feature_calculating.K_uos import uos
import numpy as np
from stockstats import StockDataFrame


def fill(df, ktype):
    stock = StockDataFrame.retype(df)
    n = 5
    df = BBANDS(df, 20)
    # df = CCI(df, 14)
    df['cci'] = stock.get('cci')
    df = ForceIndex(df, 13)
    df = EMV(df, n)
    df = EWMA(df, n)
    df = index_sh.fill(df, ktype)
    #    df = price_change.fill(df,5)
    #    df = price_change.fill(df,10)
    #    df = price_change.fill(df,20)
    df = macd.fill(df)
    df = SMA(df, 30)
    df = SMA(df, 20)
    df = SMA(df, 10)
    df = SMA(df, 5)
    df['kdjk'] = stock.get('kdjk')
    df['kdjd'] = stock.get('kdjd')
    df['kdjj'] = stock.get('kdjj')
    df['dma'] = stock.get('dma')

    #df['atr'] = stock.get('atr')
    df = w_R_rate.w_R_rate(df, 10)
    df = w_R_rate.w_R_rate(df, 28)
    df = uos(df)
    df.replace([np.inf, -np.inf], np.nan)
    return df


def fill_db_5min(df, ktype):
    n = 5
    stock = StockDataFrame.retype(df)

    df = BBANDS(df, 20)
    df['cci'] = stock.get('cci')
    df = ForceIndex(df, 13)
    df = EMV(df, n)
    df = EWMA(df, n)
    #    df = index_sh.fill(df,ktype)
    #    df = price_change.fill(df,5)
    #    df = price_change.fill(df,10)
    #    df = price_change.fill(df,20)
    df = macd.fill(df)
    df = uos(df)
    df = SMA(df, 30)
    df = SMA(df, 20)
    df = SMA(df, 10)
    df = SMA(df, 5)
    df = w_R_rate.w_R_rate(df, 10)
    df = w_R_rate.w_R_rate(df, 28)
    df['kdjk'] = stock.get('kdjk')
    df['kdjd'] = stock.get('kdjd')
    df['kdjj'] = stock.get('kdjj')
    df['dma'] = stock.get('dma')
    df['atr'] = stock.get('atr')
    df.replace([np.inf, -np.inf], np.nan)
    return df
