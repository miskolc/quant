# greg.chen - 2018/4/24

import tushare as ts

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.log.quant_logging import quant_logging as logging


# collect k_data from tushare and save into db
@exc_time
def collect_single(code, start, end, table_name='k_data'):
    try:
        logging.logger.debug(code)
        data = ts.get_k_data(code, start=start, end=end)
        data['code'] = code
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logging.logger.error(e)


