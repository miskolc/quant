# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06

from quant.common_tools.decorators import exc_time, error_handler
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.common_tools.decorators import exc_time
import tushare as ts
from quant.dao.k_data.k_data_dao import k_data_dao
import pandas as pd
from quant.log.quant_logging import logger
from datetime import datetime
from quant.common_tools.datetime_utils import get_current_date
from quant.dao.basic.stock_basic_dao import stock_performance_dao

'''
    esp,每股收益
    eps_yoy,每股收益同比(%)
    bvps,每股净资产
    roe,净资产收益率(%)
    epcf,每股现金流量(元)
    net_profits,净利润(万元)
    profits_yoy,净利润同比(%)
    report_date,发布日期
'''


@exc_time
def collect_quarter_all(start, end, year, quarter):
    df_hs_codes = ts.get_hs300s()

    for code in df_hs_codes['code'].values:
        collect_quarter(code, start, end, year, quarter)


def collect_quarter(code, start, end, year, quarter):
    data = k_data_dao.get_k_data(code, start, end, cal_next_direction=False)
    data_report = stock_performance_dao.get_by_code(code, year, quarter)

    for index, row in data.iterrows():
        try:
            dict = [{
                'code': code,
                'date': row['date'],
                'eps': data_report['eps'].values[0],
                'eps_yoy': data_report['eps_yoy'].values[0],
                'bvps': data_report['bvps'].values[0],
                'roe': data_report['roe'].values[0],
                'epcf': data_report['epcf'].values[0],
                'net_profits': data_report['net_profits'].values[0],
                'profits_yoy': data_report['profits_yoy'].values[0]
            }]

            df = pd.DataFrame(dict)

            df.to_sql('k_data_stock_performance', dataSource.mysql_quant_engine, if_exists='append',
                      index=False)
        except Exception as e:
            logger.error("code:%s, error:%s" % (code, repr(e)))


@exc_time
def collect_quarter_all_daily():
    year, quarter = cal_quarter_by_date(get_current_date())

    collect_quarter_all(year, quarter, get_current_date(), get_current_date())


def cal_quarter_by_date(date):
    current_date = datetime.strptime(date, "%Y-%m-%d").date()
    year = current_date.year
    month = current_date.month

    quarter = None
    if 1 <= month <= 3:
        year = year - 1
        quarter = 4
    elif 3 < month <= 6:
        quarter = 1
    elif 6 < month <= 9:
        quarter = 2
    elif 9 < month <= 12:
        quarter = 3

    return year, quarter
