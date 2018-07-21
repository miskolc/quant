# -*- coding: UTF-8 -*-
# ae.h - 2018/4/23
import functools
import traceback

from log.quant_logging import logger
import time


def exc_time(func):
    @functools.wraps(func)
    def fn(*args, **kv):
        start_time = time.time()
        tmp = func(*args, **kv)
        end_time = time.time()

        if not kv:
            logger.debug(
                "%s executed,  elapsed time: %.2f ms" % (func.__name__, (end_time - start_time) * 1000))
        else:
            logger.debug("%s executed, kv:%s,  elapsed time: %.2f ms" % (func.__name__, str(kv), (end_time - start_time) * 1000))
        return tmp

    return fn


def error_handler(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kv):
            try:
                return func(*args, **kv)
            except Exception as e:
                logger.error('%s failed, kv: %s' % (func.__name__, str(kv)))
                logger.error(traceback.format_exc())
                return default

        return wrapper

    return decorator
