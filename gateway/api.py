# ae_h - 2018/7/9
import os
import sys

from gateway.errors import AppError
from gateway.handler.static_resource_handler import StaticResourceHandler
from gateway.middleware.static_middleware import StaticMiddleware

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

from gateway.handler.k_data_handler import KDataHandler
import gateway.handler.position_handler as position

import falcon
from gateway.handler.index_handler import IndexHandler
from gateway.middleware.jason_validator import RequireJSON
from gateway.middleware.json_translater import JSONTranslator

# debug script: gunicorn -b 127.0.0.1:8000 --reload api:api

api = falcon.API(middleware=[RequireJSON(), JSONTranslator()])

k_data_test = KDataHandler()

api.add_route('/', IndexHandler())
api.add_static_route('/static', CURRENT_DIR+'/static/dist')
#api.add_route('/static/js/{filename}', StaticResourceHandler())
#api.add_route('/static/css/{filename}', StaticResourceHandler())
#api.add_route('/static/fonts/{filename}', StaticResourceHandler())


api.add_route('/k', k_data_test)
api.add_route('/position', position.Collection())
api.add_route('/position/{code}', position.PositionItemHandler())
api.add_route('/position/search', position.PositionSearchHandler())

api.add_error_handler(AppError, AppError.handle)

