from app.custom_feature_calculating.BBANDS import BBANDS
from app.custom_feature_calculating.CCI import CCI
from app.custom_feature_calculating.EMV import EMV
from app.custom_feature_calculating.EWMA import EWMA
from app.custom_feature_calculating.SMA import SMA
import app.custom_feature_calculating.pre_close as pre_close
import app.custom_feature_calculating.index_sh as index_sh
import app.custom_feature_calculating.price_change as price_change
from app.custom_feature_calculating.FI import ForceIndex


def fill_for_line_regression(df):
    n = 5
    df = BBANDS(df, 20)
    df = CCI(df, 20)
    df = ForceIndex(df, 13)
    df = EMV(df, n)
    df = EWMA(df, n)
    df = SMA(df, 5)
    df = SMA(df, 10)
    df = SMA(df, 20)
    df = pre_close.fill(df)
    df = index_sh.fill(df)
    df = price_change.fill(df,5)
    df = price_change.fill(df,10)
    df = price_change.fill(df,20)
    return df


def fill_for_line_regression_predict(df):
    n = 5
    df = BBANDS(df, 20)
    df = CCI(df, 20)
    df = ForceIndex(df, 13)
    df = EMV(df, n)
    df = EWMA(df, n)
    df = pre_close.fill(df)
    df = index_sh.fill(df)
    df = price_change.fill(df,5)
    df = price_change.fill(df,10)
    df = price_change.fill(df,20)
    return df
