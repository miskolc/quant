from datetime import datetime
import tushare as ts
from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.feature_utils.feature_collector import collect_features
from quant.dao.k_data.k_data_dao import k_data_dao

@exc_time
def collect_single(code, start, end, table_name='k_data_tech_feature'):
    data = k_data_dao.get_k_data(code, start=start, end=end, cal_next_direction=False)

    data, features = collect_features(data)

    features.append('code')
    features.append('date')
    data = data[features]
    data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)

@exc_time
def collect_single_daily(code, table_name='k_data_tech_feature'):
    data = ts.get_k_data(code)
    data['code'] = code
    data = data.tail(100)
    data, features = collect_features(data)

    features.append('code')
    features.append('date')
    data = data[features].tail(1)
    data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)


# 计算全量沪深300技术特征数据
@exc_time
def collect_hs300_full():
    df = ts.get_hs300s()
    now = datetime.now().strftime('%Y-%m-%d')
    for code in df['code'].values:
        try:
            collect_single(code=code, start='2015-01-01', end=now)
        except Exception as e:
            logger.error("collect technical features failed code:%s, exception:%s" % (code, repr(e)))

# 计算每天沪深300每天技术特征数据
@exc_time
def collect_hs300_daily():
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    df = ts.get_hs300s()
    for code in df['code'].values:
        try:
            collect_single_daily(code)
        except Exception as e:
            logger.error("collect technical features failed code:%s, exception:%s" % (code, repr(e)))