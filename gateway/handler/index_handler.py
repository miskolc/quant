# ae_h - 2018/7/9
import json
import pdb


class IndexHandler(object):
    def on_get(self, req, resp):
        result = {'msg': 'hello quant'}
        resp.context['result'] = result
