# greg.chen - 2018/5/19


class DataSource(object):
    @property
    def mysql_quant_engine(self):
        return self._mysql_quant_engine

    @mysql_quant_engine.setter
    def mysql_quant_engine(self, value):
        self._mysql_quant_engine = value


dataSource = DataSource()
