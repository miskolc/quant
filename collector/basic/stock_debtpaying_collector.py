# ae_h - 2018/7/20
from common_tools.datetime_utils import get_current_quater
from common_tools.decorators import exc_time, error_handler
from datetime import datetime
import tushare as ts

from dao import dataSource
from dao.basic.stock_basic_dao import stock_basic_dao

'''
code,代码
name,名称
currentratio,流动比率
quickratio,速动比率
cashratio,现金比率
icratio,利息支付倍数
sheqratio,股东权益比率
adratio,股东权益增长率

'''



@exc_time
def collect_all():
    debtpaying_df = ts.get_debtpaying_data(datetime.now().year, get_current_quater(datetime.now()) - 2)
    # debtpaying_df.fillna(0, inplace=True)

    debtpaying_df.to_sql('stock_debtpaying', dataSource.mysql_quant_engine, if_exists='append', index=False)



if __name__ == '__main__':
    collect_all()
