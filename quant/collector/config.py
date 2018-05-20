# greg.chen - 2018/5/20

import os


class Config(object):
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
if env is not None and config.has_key(env):
    config["default"] = config["env"]
    pass
else:
    config["default"] = DevelopmentConfig
