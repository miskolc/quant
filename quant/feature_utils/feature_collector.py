# ae.h - 2018/5/21
from inspect import getmembers, isfunction
from quant.feature_utils import momentum_indicators, overlaps_studies
import tushare as ts
import pandas as pd
import re

# os_ip_modules = __import__('overlaps_studies')
#
# mi_ip_modules = __import__('momentum_indicators')

df = ts.get_k_data('600179', ktype='D', start='2015-01-01', end='2018-05-05')

momentum_list = [m for m in getmembers(momentum_indicators) if isfunction(m[1])]
overlaps_list = [o for o in getmembers(overlaps_studies) if isfunction(o[1])]

func_list = momentum_list + overlaps_list

for func in func_list:
    if hasattr(momentum_indicators, func[0]) or hasattr(overlaps_studies, func[0]):
        col_name = re.match(r'(^.{4})(.{0,})', func[0]).group(2)
        func_feature = func[1](df)
        if isinstance(func_feature, pd.core.series.Series):
            df[col_name] = func_feature
        else:
            df = df.join(func_feature)
df.to_csv('/Users/yw.h/Desktop/resultt.csv')



