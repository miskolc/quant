# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06


from quant.common_tools.decorators import exc_time, error_handler
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.common_tools.decorators import exc_time
from quant.dao.basic.stock_industry_dao import stock_industry_dao
from quant.crawler.sina_finance_api import sina_finance_api
import time


def collect_all():
    df_stock = stock_industry_dao.get_list()
    for index, row in df_stock.iterrows():
        data = sina_finance_api.get_stock_structure_by_code(row["code"])
        time.sleep(1)
        if data is not None:
            data.to_sql('stock_structure', dataSource.mysql_quant_engine, if_exists='append', index=False)
