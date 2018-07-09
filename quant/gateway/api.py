# ae_h - 2018/7/9
import os
import sys

from quant.gateway.handler.k_data_handler import KDataHandler

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)
import falcon
from quant.gateway.handler.index_handler import IndexHandler
from quant.gateway.middleware.jason_validator import RequireJSON
from quant.gateway.middleware.json_translater import JSONTranslator

api = falcon.API(middleware=[RequireJSON(), JSONTranslator()])

index_handler = IndexHandler()
k_data_test = KDataHandler()

api.add_route('/', index_handler)
api.add_route('/k', k_data_test)



