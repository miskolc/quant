# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import requests
import json
import pandas as pd

from common_tools.decorators import exc_time
from log.quant_logging import logger
from lxml import etree
import io


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
              "&jsName=quote_123&_g=0.628606915911589&_=1528262954509" % ('.' + bk_code + '1', self.token)

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
            df = df.append({'bk_code': bk_code, 'bk_name': bk_name, 'code': code, 'name': name}, ignore_index=True)

        return df

    @exc_time
    def get_stock_basic(self, code):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

        url = 'http://data.eastmoney.com/stockdata/%s.html' % code
        response = requests.get(url, headers=headers)
        content = response.content.decode('gbk')

        buf = io.StringIO(content)
        line = buf.readline()

        df = pd.DataFrame(
            columns=['report_date','pe', 'pb', 'eps', 'roe', 'profits_yoy', 'income_yoy', 'total_market', 'total_assets',
                     'total_liabilities', 'retained_profits'])
        dict = {"code": code}
        while line is not None and len(line) > 0:
            line = buf.readline()

            if line.find('var hypmData') > -1:
                line = line.replace("var hypmData=", '')
                line = line.replace(";", '')
                data = json.loads(line)
                dict['pe'] = data["Data"][0]["PERation"]
                dict['pb'] = data["Data"][0]["PBRation"]
                dict['total_market'] = data["Data"][0]["TotalMarketValue"]

                if dict['pe'] == '-':
                    dict['pe'] = None

                if dict['pb'] == '-':
                    dict['pb'] = None

            if line.find("var cwzyData") > -1:
                line = line.replace("var cwzyData =", '')

                data = json.loads(line)
                # 基本每股收益
                dict['report_date'] = data[0]["ReportDate"]
                # 基本每股收益
                dict['eps'] = data[0]["BasicEPS"]
                # 净资产收益率
                dict['roe'] = data[0]["WeightedYieldOnNetAssets"]
                # 净利润同比(%)
                dict['profits_yoy'] = data[0]["ProfitsYOYRate"]
                if dict['profits_yoy'] == "\\" or dict['profits_yoy'] == '':
                    dict['profits_yoy'] = None

                # 营收同比率(%)
                dict['income_yoy'] = data[0]["IncomeYOYRate"]
                # 总资产
                dict['total_assets'] = data[0]["totalAssets"]
                # 总负债
                dict['total_liabilities'] = data[0]["totalLiabilities"]
                # 净利润
                dict['retained_profits'] = data[0]["retainedProfits"]



        df = df.append(dict, ignore_index=True)

        return df

    @exc_time
    def get_industry_vol(self, bkcode):
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=%s' \
              '&sty=FDPBPFB&st=z&sr=&p=&ps=&cb=jQuery17205845203068985219_1533009446115&js=([[(x)]])' \
              '&token=7bc05d0d4c3c22ef9fca8c2a912d779c&_=1533009446214' % bkcode
        response = requests.get(url)
        content = response.content.decode('utf-8')
        bracket_start_index = content.find('[[') + 2
        bracket_end_index = content.find(']]') + 2
        content = content[bracket_start_index:bracket_end_index]
        content = content.split(',')
        print(content[9])

    @exc_time
    def get_concept_board(self):

        concept_dict = {}

        url = 'http://quote.eastmoney.com/center/sidemenu.json'
        resp = requests.get(url=url)
        content = resp.content.decode('utf-8')
        concept_start_index = content.find('概念板块')
        concept_end_index = content.find('地域板块')
        content = content[concept_start_index:concept_end_index]
        content = '[' + content[content.find('{'):content.rfind('}') - 1] + ']'
        content_json = json.loads(content)

        for item in content_json:
            concept_dict[item['key'].split('-')[1]] = item['title']

        return concept_dict


east_money_api = EastMoneyApi()

