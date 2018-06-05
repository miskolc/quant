# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/1

from datetime import datetime,timedelta

DATE_FORMAT = '%Y-%m-%d'


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT)

def get_next_date(days):
    return (datetime.now() + timedelta(days)).strftime(DATE_FORMAT)