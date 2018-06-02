# -*- coding: UTF-8 -*-
# ae.h - 2018/4/23
import functools
from quant.log.quant_logging import logger
import time


def exc_time(func):
    @functools.wraps(func)
    def fn(*args, **kv):
        start_time = time.time()
        tmp = func(*args, **kv)
        end_time = time.time()
        logger.debug("%s executed, elapsed time: %.2f ms" % (func.__name__, (end_time - start_time) * 1000))
        return tmp

    return fn
