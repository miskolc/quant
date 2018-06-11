from sqlalchemy import create_engine, MetaData
import tushare as ts
from quant.config import default_config
from quant.dao import dataSource
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.common_tools.datetime_utils import get_current_date
from quant.feature_utils.custome_features import cal_mavol30
from quant.feature_utils.overlaps_studies import cal_ma30,cal_ma60

def init_db():

    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=10, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine
        dataSource.mysql_quant_conn = mysql_quant_engine.connect()
        dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)


def cal_singal_stock(code):
    print("execute code: %s" % code)
    try:
        data = ts.get_k_data(code)

        data["mavol30"] = cal_mavol30(data)
        data["ma60"] = cal_ma60(data)

        current_price = data['close'].tail(1).values[0]
        current_val = data['volume'].tail(1).values[0]

        current_ma60 = data['ma60'].tail(1).values[0]
        current_mavol30 = data['mavol30'].tail(1).values[0]

        if current_price > current_ma60 and current_val * 1.5 < current_mavol30:

            return code
    except Exception:
        pass

def abnormal_val(data, code):

    try:
        start_engine = {'date':None, 'volume':None}
        for index,row in data.iterrows():
            current_mavol30 = row['mavol30']
            current_val = row['volume']
            current_ma60 = row['ma60']
            current_price = row['close']
            pre_close = row['pre_close']

            if  pre_close*1.02 < current_price and current_val  > current_mavol30 * 3:

                return code, row['date'], current_val

        return None,None,None
    except Exception:
        pass

if __name__ == '__main__':
    #init_db()

    df = ts.get_hs300s()
    #df['code'].values
    for code in ['603630',]:
        try:
            #print(code)
            data = ts.get_k_data(code, start='2017-01-01')
            data["mavol30"] = cal_mavol30(data)
            data["ma30"] = cal_ma30(data)
            data["ma60"] = cal_ma60(data)
            data['pre_close'] = data['close'].shift();
            #data['p_change'] = ((data['close'] - data['pre_close']) / data['pre_close'])

            data = data.tail(30)
            #print(data[['date','close','ma30', 'volume', 'mavol30']])

            code, date, volume = abnormal_val(data, code)

            #code = cal_singal_stock('002661')

            if code is None:
                continue

            current_price = data['close'].tail(1).values[0]
            current_val = data['volume'].tail(1).values[0]
            current_ma60 = data['ma60'].tail(1).values[0]
            current_ma30 = data['ma30'].tail(1).values[0]
            current_mavol30 = data['mavol30'].tail(1).values[0]

            if current_price> current_ma30 and current_price > current_ma60:
                print(code, date)

        except Exception:
            pass