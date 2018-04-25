# ae.h - 2018/4/23
import functools
from datetime import datetime


def exc_time(func):
    @functools.wraps(func)
    def fn(*args, **kv):
        start_time = datetime.now()
        tmp = func(*args, **kv)
        end_time = datetime.now()
        print('\n')
        print("%s executed in %s ms" % (func.__name__, (end_time - start_time) * 1000))
        return tmp

    return fn
