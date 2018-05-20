# greg.chen - 2018/4/24

import tushare as ts

from app.collector.collector_logging import collector_logging as logging
from app.dao.data_source import dataSource


# collect k_data from tushare and save into db
def collect(code, start, end, table_name='k_data'):
    try:
        logging.logger.debug(code)
        data = ts.get_k_data(code, start=start, end=end)
        data['code'] = code
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        pass
        logging.logger.error(e)


