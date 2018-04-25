#!/usr/bin/python
# -*- coding: utf-8 -*-

# engine.py
#


from __future__ import print_function

from sqlalchemy import create_engine

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'root'
db_pass = 'root'
db_name = 'quantitative'

def create():
    engine = create_engine(
        "mysql+mysqldb://" + db_user + ":" + db_pass + "@" + db_host + "/" + db_name + "?charset=utf8",
        encoding='utf8', convert_unicode=True)

    return engine
