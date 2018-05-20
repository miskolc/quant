# greg.chen - 2018/5/20

import os


class Config(object):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    db_host = '192.168.1.131:3306'
    db_user = 'root'
    db_pass = 'aGiOxoNrqbeT7XWW'
    db_name = 'quant'

    DATABASE_QUANT_URI = "mysql+mysqldb://" + db_user + ":" + db_pass + "@" + db_host + "/" + db_name + "?charset=utf8"


class TestingConfig(Config):
    DEBUG = False

    db_host = '192.168.1.131:3306'
    db_user = 'root'
    db_pass = 'aGiOxoNrqbeT7XWW'
    db_name = 'quant'

    DATABASE_QUANT_URI = "mysql+mysqldb://" + db_user + ":" + db_pass + "@" + db_host + "/" + db_name + "?charset=utf8"


class RemoteDevelopmentConfig(Config):
    DEBUG = True

    db_host = 's1.natapp.cc:33068'
    db_user = 'root'
    db_pass = 'aGiOxoNrqbeT7XWW'
    db_name = 'quant'

    DATABASE_QUANT_URI = "mysql+mysqldb://" + db_user + ":" + db_pass + "@" + db_host + "/" + db_name + "?charset=utf8"


config = {
    "development": DevelopmentConfig,
    "remote-development": RemoteDevelopmentConfig,
    "default": None
}

env = os.getenv('quant_env')
if env is not None and config.has_key(env):
    config["default"] = config["env"]
    pass
else:
    config["default"] = DevelopmentConfig
