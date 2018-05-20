#!/usr/bin/python
# -*- coding: utf-8 -*-

# data_source.py
#


class DataSource(object):
    @property
    def mysql_quant_engine(self):
        return self._mysql_quant_engine

    @mysql_quant_engine.setter
    def mysql_quant_engine(self, value):
        self._mysql_quant_engine = value


dataSource = DataSource()

'''
mysql_quant_engine = None
default_config = config['default']

# 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
if default_config.DATABASE_QUANT_URI:
    # 使用单例模式保存数据库engine
    mysql_quant_engine = create_engine(
        default_config.DATABASE_QUANT_URI,
        encoding='utf8', convert_unicode=True)
'''
