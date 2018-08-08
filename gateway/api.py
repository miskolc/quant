# ae_h - 2018/7/9
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

import falcon

from gateway.handler.stock_handler import StockHandler
import gateway.handler.position_handler as position
import gateway.handler.strategy_handler as strategy
import gateway.handler.target_handler as target
from gateway.handler.index_handler import IndexHandler
from gateway.middleware.jason_validator import RequireJSON
from gateway.middleware.json_translater import JSONTranslator
from gateway.errors import AppError



# debug script: gunicorn -b 127.0.0.1:8000 --reload api:api

api = falcon.API(middleware=[RequireJSON(), JSONTranslator()])

api.add_route('/', IndexHandler())
api.add_static_route('/static', CURRENT_DIR + '/static/dist')
api.add_static_route('/static/js', CURRENT_DIR + '/static/dist/static/js')
api.add_static_route('/static/css', CURRENT_DIR + '/static/dist/static/css')
api.add_static_route('/static/fonts', CURRENT_DIR + '/static/dist/static/fonts')

api.add_route('/stock/{code}',StockHandler())
api.add_route('/strategy/search', strategy.StrategySearchHandler())

api.add_route('/position/{strategy_code}/{code}', position.PositionHandler())
api.add_route('/position', position.Collection())
api.add_route('/position/search', position.PositionSearchHandler())

api.add_route('/target/{id}', target.TargetHandler())
api.add_route('/target/search', target.TargetSearchHandler())
api.add_route('/target', target.Collection())

api.add_error_handler(Exception, AppError.handle)
