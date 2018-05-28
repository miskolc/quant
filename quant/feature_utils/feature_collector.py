# ae.h - 2018/5/21
from inspect import getmembers, isfunction
import os
from quant.feature_utils import momentum_indicators, overlaps_studies, volume_indicators, cycle_indicators, \
    price_transform, volatility_indicators, custome_features
import tushare as ts
import pandas as pd
import re

# os_ip_modules = __import__('overlaps_studies')
#
# mi_ip_modules = __import__('momentum_indicators')

root_path = os.path.dirname(os.path.abspath(__file__))
# print(root_path)
# feature_path = os.path.join(root_path, 'feature_utils/')


momentum_list = [m for m in getmembers(momentum_indicators) if isfunction(m[1])]
overlaps_list = [o for o in getmembers(overlaps_studies) if isfunction(o[1])]
volume_list = [v for v in getmembers(volume_indicators) if isfunction(v[1])]
cycle_list = [c for c in getmembers(cycle_indicators) if isfunction(c[1])]
price_list = [p for p in getmembers(price_transform) if isfunction(p[1])]
volatility_list = [l for l in getmembers(volatility_indicators) if isfunction(l[1])]
custome_list = [u for u in getmembers(custome_features) if isfunction(u[1])]

func_list = momentum_list + overlaps_list + volume_list + volume_list + cycle_list + price_list + volatility_list + custome_list


def get_col_name_list():
    col_name_list = []
    for func in func_list:
        col_name = re.match(r'(^.{4})(.{0,})', func[0]).group(2)
        col_name_list.append(col_name)

    return col_name_list


def collect_features(df):
    col_list = []
    for func in func_list:
        if hasattr(momentum_indicators, func[0]) or hasattr(overlaps_studies, func[0]) or hasattr(volume_indicators, func[0]) or hasattr(cycle_indicators, func[0]) or hasattr(price_transform, func[0]) or hasattr(volatility_indicators, func[0]) or hasattr(custome_features, func[0]):
            col_name = re.match(r'(^.{4})(.{0,})', func[0]).group(2)
            func_feature = func[1](df)
            if isinstance(func_feature, pd.core.series.Series):
                df[col_name] = func_feature
                col_list.append(col_name)
            else:
                df = df.join(func_feature)
                col_list.append(list(func_feature.columns.values))
    # df.to_csv('/Users/yw.h/Desktop/resultt.csv')
    # print(col_list)
    return df, col_list


# df = ts.get_k_data('600179', ktype='D')
# collect_features(df)



# big_list = os.listdir(root_path)
# # # print(big_list)
# big_list.remove('__init__.py')
# big_list.remove('__pycache__')
# big_list.remove('feature_collector.py')
# # print(big_list)
#
#
# module_list = []
# for module in big_list:
# #     # print(module)
#     print(__import__(module))
#     # print(getmembers(dir_path+module))
#     # print([m for m in getmembers(dir_path+module) if isfunction(m[1])])
#     # module_list.append([m for m in getmembers(module) if isfunction(m[1])])
#
# # print(module_list)


