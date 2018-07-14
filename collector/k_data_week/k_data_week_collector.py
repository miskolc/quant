# -*- coding: UTF-8 -*-
# greg.chen - 2018/4/24

from datetime import datetime
import tushare as ts
from common_tools import exc_time
from dao.data_source import dataSource
from log.quant_logging import logger
from dao.basic.stock_industry_dao import stock_industry_dao


# collect k_data from tushare and save into db
@exc_time
def collect_single(code, start, end, table_name='k_data_week'):
    try:
        data = ts.get_k_data(code, start=start, end=end, ktype='W')
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.dropna()
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_weekly(code, table_name='k_data'):
    try:
        data = ts.get_k_data(code, ktype='W')
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.tail(1)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)



# 抓取所有k_data数据
@exc_time
def collect_all():
    now = datetime.now().strftime('%Y-%m-%d')
    df_industry = stock_industry_dao.get_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single(code=code, start='2015-01-01', end=now)


# 抓取沪深每天K_data_daily数据
@exc_time
def collect_all_weekly(table_name='k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    df_industry = stock_industry_dao.get_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single_weekly(code=code, table_name=table_name)