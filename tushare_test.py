# ae_h - 2018/7/20
import tushare as ts
from datetime import datetime
from common_tools.datetime_utils import get_current_quater


# basic_df = ts.get_stock_basics()
# basic_df.to_csv('stock_basic.csv', encoding='utf-8')

try:
    debtpaying_df = ts.get_debtpaying_data(datetime.now().year, get_current_quater(datetime.now()))
except:
    debtpaying_df = ts.get_debtpaying_data(datetime.now().year, get_current_quater(datetime.now())-2)

print(debtpaying_df)
debtpaying_df.to_csv('debtpaying.csv', encoding='utf-8')
