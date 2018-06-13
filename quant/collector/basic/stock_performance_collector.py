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
def collect_single_quarter(year, quarter, start, end):
    data = ts.get_report_data(year, quarter)
    data['year'] = year
    data['quarter'] = quarter
    data['report_date'] = str(year) + '-' + data['report_date']
    data.to_sql('stock_performance', dataSource.mysql_quant_engine, if_exists='append', index=False)




@exc_time
def collect_quarter_all(year, quarter, start, end):
    data_report = ts.get_report_data(year, quarter)
    data_report.to_csv('result.csv')
    df_hs_codes = ts.get_hs300s()

    for code in df_hs_codes['code'].values:
        collect_single(data_report, code, start, end)


def collect_single(data_report, code, start, end):
    data_report_code = data_report.query[data_report['code'] == code].tail(1)

    if data_report_code is None:
        return

    #data_report_code = data_report_code.fillna(0)
    data = k_data_dao.get_k_data(code, start, end, cal_next_direction=False)

    for index, row in data.iterrows():
        df_item = pd.DataFrame(
            columns=['code', 'date', 'eps', 'eps_yoy', 'bvps', 'roe', 'epcf', 'net_profits',
                     'profits_yoy'])

        df_item['code'] = code
        df_item['date'] = row['date']
        try:

            df_item['eps'] = data_report_code['eps'].values[0]
            df_item['eps_yoy'] = data_report_code['eps_yoy'].values[0]
            df_item['bvps'] =  data_report_code['bvps'].values[0]
            df_item['roe'] =  data_report_code['roe'].values[0]
            df_item['epcf'] = data_report_code['epcf'].values[0]
            df_item['net_profits'] = data_report_code['net_profits'].values[0]
            df_item['profits_yoy'] = data_report_code['profits_yoy'].values[0]
        except Exception as e:
            logger.error("code:%s, error:%s" % (code, repr(e)))
        finally:
            df_item.to_sql('k_data_stock_performance', dataSource.mysql_quant_engine, if_exists='append',
              index=False)

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
