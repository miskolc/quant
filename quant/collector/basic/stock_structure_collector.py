# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06


from quant.common_tools.decorators import exc_time, error_handler
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.common_tools.decorators import exc_time
from quant.dao.basic.stock_industry_dao import stock_industry_dao
from quant.crawler.sina_finance_api import sina_finance_api
import time
import tushare as ts


def collect_all():
    df = ts.get_hs300s()
    for code in df['code'].values:
        try:
            collect_single(code)
            time.sleep(0.5)
        except Exception as e:
            logger.error(repr(e))


def collect_single(code, retry=0):

    if retry > 3:
        return
    try:
        data = sina_finance_api.get_stock_structure_by_code(code)
        if data is not None:
            data = data.drop_duplicates('date', 'first')
            data.to_sql('stock_structure', dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        retry += 1
        collect_single(code, retry)