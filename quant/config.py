# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/20

import os


class Config(object):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_OUTPUT_DIR = os.path.join(ROOT_DIR, 'models/output/')
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