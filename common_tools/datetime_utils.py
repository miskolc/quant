# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/1

from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'
DATE_HOUR_FORMAT = '%Y-%m-%d %H'


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT)


def get_current_date_hour():
    return datetime.now().strftime(DATE_HOUR_FORMAT)


def get_next_date(days):
    return (datetime.now() + timedelta(days)).strftime(DATE_FORMAT)
