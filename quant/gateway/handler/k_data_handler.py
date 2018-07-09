# ae_h - 2018/7/9
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.dao.k_data.k_data_dao import k_data_dao


class KDataHandler(object):
    def on_get(self, req, resp):
        data = k_data_dao.get_k_data('600196', start='2018-01-01', end='2018-07-01')
        df = data[['date', 'open', 'close', 'low', 'high', 'volume', 'pre_close']]
        df_json = df.to_json(orient='records')
        print(df_json)

        resp.context['result'] = df_json
