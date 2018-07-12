# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/20
import logging
import logging.handlers
import os
from config import default_config


logger_name="quant"

logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

logging_format = logging.Formatter(
    '%(asctime)s - %(process)d - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

if default_config.DEBUG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging_format)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

if not os.path.exists("log"):
    os.mkdir("log")

file_handler = logging.handlers.TimedRotatingFileHandler('log/%s.log' % logger_name,
                                                         encoding='UTF-8', when='D',
                                                         interval=1,
                                                         backupCount=7)
file_handler.setFormatter(logging_format)
file_handler.setLevel(logging.ERROR)
logger.addHandler(file_handler)
