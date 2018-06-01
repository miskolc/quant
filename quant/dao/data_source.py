# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19


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


dataSource = DataSource()

