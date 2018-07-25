# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/1

from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'
DATE_HOUR_FORMAT = '%Y-%m-%d %H'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_current_date(args=None):
    if args:
        return args.strftime(DATE_FORMAT)
    else:
        return datetime.now().strftime(DATE_FORMAT)


def get_current_date_hour():
    return datetime.now().strftime(DATE_HOUR_FORMAT)


def get_next_date(days, args=None):
    if args:
        args = convert_to_datetime(args)
        return (args + timedelta(days)).strftime(DATE_FORMAT)
    else:
        return (datetime.now() + timedelta(days)).strftime(DATE_FORMAT)


def convert_to_datetime(date):
    return datetime.strptime(date, DATE_FORMAT)


def get_current_quater(current_datetime):
    return datetime.now().month // 3 + 1
