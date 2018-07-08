# ae.h - 2018/5/21
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)
import os
import re
from inspect import getmembers, isfunction

import pandas as pd

from quant.feature_utils import momentum_indicators, overlaps_studies, volume_indicators, cycle_indicators, \
    price_transform, volatility_indicators, custome_features, pattern_recognition, statistic_functions

root_path = os.path.dirname(os.path.abspath(__file__))

momentum_list = [m for m in getmembers(momentum_indicators) if isfunction(m[1])]
overlaps_list = [o for o in getmembers(overlaps_studies) if isfunction(o[1])]
volume_list = [v for v in getmembers(volume_indicators) if isfunction(v[1])]
cycle_list = [c for c in getmembers(cycle_indicators) if isfunction(c[1])]
price_list = [p for p in getmembers(price_transform) if isfunction(p[1])]
volatility_list = [l for l in getmembers(volatility_indicators) if isfunction(l[1])]
custome_list = [u for u in getmembers(custome_features) if isfunction(u[1])]
stastic_list = [s for s in getmembers(statistic_functions) if isfunction(s[1])]
# pattern_list = [r for r in getmembers(pattern_recognition) if isfunction(r[1])]

func_list = momentum_list + overlaps_list + volume_list + volume_list + cycle_list + price_list + volatility_list + custome_list + stastic_list


def get_col_name_list(func_list):
    col_name_list = []
    for func in func_list:
        col_name = re.match(r'(^.{4})(.{0,})', func[0]).group(2)
        col_name_list.append(col_name)
    print(col_name_list)
    return col_name_list


def collect_features(df):
    col_list = []
    for func in func_list:
        if hasattr(momentum_indicators, func[0]) or hasattr(overlaps_studies, func[0]) or hasattr(volume_indicators,
                                                                                                  func[0]) \
                or hasattr(cycle_indicators, func[0]) or hasattr(price_transform, func[0]) or hasattr(
            volatility_indicators, func[0]) \
                or hasattr(custome_features, func[0]) or hasattr(statistic_functions, func[0]):
            col_name = re.match(r'(^.{4})(.{0,})', func[0]).group(2)
            func_feature = func[1](df)

            if func_feature is None:
                continue

            if isinstance(func_feature, pd.core.series.Series):
                df[col_name] = func_feature
                col_list.append(col_name)
            else:
                df = df.join(func_feature)
                col_names_list = func_feature.columns.values
                for col in col_names_list:
                    col_list.append(col)
    # df.to_csv('resultt.csv')
    df = df.dropna()

    col_list = list(set(col_list))
    return df, col_list
