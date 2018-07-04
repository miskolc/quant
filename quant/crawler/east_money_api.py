# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import requests
import json
import pandas as pd
from quant.log.quant_logging import logger
from quant.dao.data_source import dataSource

class EastMoneyApi:
    cb = 'jQuery112408109796406405649_1528256941912'
    token = '4f1862fc3b5e77c150a2b985b12db0fd'

    '''
        从东方财富爬取各类板块编号
    '''
    def get_industry_all(self):
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?' \
              'cb=%s&type=CT&token=%s&' \
              'js=({data:[(x)],recordsTotal:(tot),recordsFiltered:(tot)})' \
              '&cmd=C._BKHY&sty=FPGBKI&st=(ChangePercent)&sr=-1&p=1&ps=1000' \
              '&_=1528258870269' % (self.cb, self.token)

        response = requests.get(url)
        content = response.content.decode('utf-8')
        start = content.index('{')
        end = content.index(')')
        content = content[start:end]
        content = content.replace('data', '"data"')
        content = content.replace('recordsTotal', '"recordsTotal"')
        content = content.replace('recordsFiltered', '"recordsFiltered"')

        data = json.loads(content)

        code_list = []
        name_list = []
        for item in data["data"]:
            arr = item.split(',')
            code_list.append(arr[1])
            name_list.append(arr[2])

        dict = {
            "code": code_list,
            "name": name_list
        }

        df = pd.DataFrame(dict)

        return df

    '''
        从东方财富爬取各类板块的股票列表
    '''
    def get_stock_industry_by_bk_code(self, bk_code, bk_name):
        url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT" \
              "&cmd=C%s&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=1000" \
              "&js=var UGPKIszR={rank:[(x)],pages:(pc),total:(tot)}&token=%s" \
              "&jsName=quote_123&_g=0.628606915911589&_=1528262954509" % ('.' + bk_code +'1', self.token)

        response = requests.get(url)
        content = response.content.decode('utf-8')

        start = content.index('{')
        end = content.index('}') + 1
        content = content[start:end]
        content = content.replace('rank', '"rank"')
        content = content.replace('pages', '"pages"')
        content = content.replace('total', '"total"')

        data = json.loads(content)


        df = pd.DataFrame(columns=['bk_code', 'bk_name', 'code', 'name'])

        for item in data["rank"]:
            arr = item.split(',')
            code = arr[1]
            name = arr[2]
            df = df.append({'bk_code': bk_code, 'bk_name':bk_name, 'code':code, 'name': name}, ignore_index=True)

        return df


east_money_api = EastMoneyApi()
