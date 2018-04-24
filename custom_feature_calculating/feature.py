from custom_feature_calculating.BBANDS import BBANDS
from custom_feature_calculating.CCI import CCI
from custom_feature_calculating.FI import ForceIndex
from custom_feature_calculating.EMV import EMV
from custom_feature_calculating.EWMA import EWMA
from custom_feature_calculating.SMA import SMA

def fill_for_line_regression(df):
    n = 5
    df = BBANDS(df, 20)
    #df = CCI(df, 20)
    df = ForceIndex(df, 13)
    df = EMV(df, n)
    df = EWMA(df, n)
    df = SMA(df, 5)
    df = SMA(df, 10)
    df = SMA(df, 20)

    return df


def fill_for_line_regression_predict(df):

    df = BBANDS(df, 20)
    df = CCI(df, 20)
    df = ForceIndex(df, 13)
    df = EMV(df, 5)
    df = EWMA(df, 5)

    return df