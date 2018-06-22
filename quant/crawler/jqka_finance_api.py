# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19
from datetime import datetime
import tushare as ts
from lxml import etree

from quant.collector.k_data.k_data_collector import collect_single
from quant.dao import dataSource
from quant.log.quant_logging import logger
import json
import requests
import pandas as pd


class JQKAApi:


    def get_data(self):
        df = ts.get_hs300s()
        now = datetime.now().strftime('%Y-%m-%d')
        for code,name in df[['code','name']].values:
            #collect_single(code=code, start='2015-01-01', end=now, table_name=table_name)
            self.get_stock_performance(code,name)



    def get_stock_performance(self,code,name):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        url = "http://basic.10jqka.com.cn/%s/finance.html#stockpage" % (code)


        r = requests.get(url, headers=headers)
        #logger.debug(r.content.decode('gbk'))
        try:
            selector = etree.HTML(r.content.decode('gbk'))

            content = selector.xpath('//*[@id="main"]/text()')[0]

            data = json.loads(content)

            df1 = pd.DataFrame(data['simple'],index=None)

            df2 = df1.T
            df = pd.DataFrame(df2.values,columns=['report_date','esp','net_profits','profits_yoy','not_net_profits','not_profits_yoy','business_income','business_income_yoy','bvps','roe','roe_tanbo',
                                            'net_debt_ratio','reservedPerShare','undistributed_profit_per_share','cash_flow_per_share','sales_gross_margin', 'inventory_turnover','sales_margin'])

            df = df.reindex(columns=['code','name','report_date','esp','net_profits','profits_yoy','not_net_profits','not_profits_yoy','business_income','business_income_yoy','bvps','roe','roe_tanbo',
                                      'net_debt_ratio','reservedPerShare','undistributed_profit_per_share','cash_flow_per_share','sales_gross_margin', 'inventory_turnover','sales_margin'])
            df['profits_yoy'] = df['profits_yoy'].str.strip('%')
            df['not_profits_yoy'] = df['not_profits_yoy'].str.strip('%')
            df['business_income_yoy'] = df['business_income_yoy'].str.strip('%')
            df['roe'] = df['roe'].str.strip('%')
            df['roe_tanbo'] = df['roe_tanbo'].str.strip('%')
            df['net_debt_ratio'] = df['net_debt_ratio'].str.strip('%')
            df['sales_gross_margin'] = df['sales_gross_margin'].str.strip('%')
            df['sales_margin'] = df['sales_margin'].str.strip('%')
            df['net_profits'] = df['net_profits'].str.strip('亿')
            df['not_net_profits'] = df['not_net_profits'].str.strip('亿')
            df['business_income'] = df['business_income'].str.strip('亿')
            df['code'] = code
            df['name'] = name

            print(df.head(13))

            return df

            #logger.debug(data)
        except Exception as e:
            logger.debug(repr(e))
            return None



jqka_finance_api = JQKAApi()
