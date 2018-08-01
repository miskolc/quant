# ae_h - 2018/7/9
import json
import pdb

import falcon


class IndexHandler(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open('static/dist/index.html', 'r') as f:
            resp.body = f.read()
