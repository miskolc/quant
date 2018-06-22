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
def collect_single_quarter(year, quarter):
    data = ts.get_report_data(year, quarter)
    data['year'] = year
    data['quarter'] = quarter
    data['report_date'] = str(year) + '-' + data['report_date']
    data.to_sql('stock_performance', dataSource.mysql_quant_engine, if_exists='append', index=False)

