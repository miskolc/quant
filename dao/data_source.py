# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19
from sqlalchemy import create_engine, MetaData

from config import default_config


class DataSource(object):

    @property
    def mysql_quant_engine(self):
        return self._mysql_quant_engine

    @mysql_quant_engine.setter
    def mysql_quant_engine(self, value):
        self._mysql_quant_engine = value


    @property
    def mysql_quant_conn(self):
        return self._mysql_quant_conn
    
    @mysql_quant_conn.setter
    def mysql_quant_conn(self, value):
        self._mysql_quant_conn = value

    @property
    def mysql_quant_metadata(self):
        return self._mysql_quant_metadata

    @mysql_quant_metadata.setter
    def mysql_quant_metadata(self, value):
        self._mysql_quant_metadata = value


    @property
    def futu_quote_ctx(self):
        return self._futu_quote_ctx

    @futu_quote_ctx.setter
    def futu_quote_ctx(self, value):
        self._futu_quote_ctx = value

dataSource = DataSource()

if default_config.DATABASE_QUANT_URI:
    # 使用单例模式保存数据库engine
    mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                       convert_unicode=True, pool_size=50, pool_recycle=1200)
    dataSource.mysql_quant_engine = mysql_quant_engine
    dataSource.mysql_quant_conn = mysql_quant_engine.connect()
    dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)


