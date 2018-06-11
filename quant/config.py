# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/20

import os


class Config(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'models/output/')
    TEMPLATE_DIR = os.path.join(ROOT_DIR, 'notification_tools/templates/')
    MAIL_FROM_ADDR = 'Q_catcher@sohu.com'
    MAIL_FROM_PWD = 'aedotpy000'
    MAIL_TO = ['aemaeth@foxmail.com', 'greg.ch@fowtech.com']
    MAIL_SMTP = 'smtp.sohu.com'
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DATABASE_QUANT_URI = "mysql+mysqldb://root:aGiOxoNrqbeT7XWW@192.168.1.131:3306/quant?charset=utf8"


class TestingConfig(Config):
    DEBUG = False
    DATABASE_QUANT_URI = "mysql+mysqldb://root:aGiOxoNrqbeT7XWW@192.168.1.131:3306/quant?charset=utf8"


class RemoteDevelopmentConfig(Config):
    DEBUG = True
    DATABASE_QUANT_URI = "mysql+mysqldb://root:aGiOxoNrqbeT7XWW@s1.natapp.cc:33068/quant?charset=utf8"


config = {
    "development": DevelopmentConfig,
    "remote-development": RemoteDevelopmentConfig,
    "testing": TestingConfig,
    "default": None
}

env = os.getenv('quant_env')

if env is not None and env in config.keys():
    config["default"] = config[env]
    pass
else:
    config["default"] = DevelopmentConfig

default_config = config['default']

# Theano require set MKL_THREADING_LAYER=GNU in environment
os.environ["MKL_THREADING_LAYER"] = "GNU"