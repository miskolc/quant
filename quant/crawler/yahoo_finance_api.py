# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import re
import time
import datetime
import requests
import pandas as pd
import io

from quant.common_tools.decorators import exc_time
from quant.log.quant_logging import logger
from lxml import etree


class YahooFinanceApi:
    def get_page_data(self, symbol):
        url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
        r = requests.get(url)
        cookie = {'B': r.cookies['B']}
        lines = r.content.decode('unicode-escape').strip().replace('}', '\n')
        return cookie, lines.split('\n')

    def find_crumb_store(self, lines):
        # Looking for,"CrumbStore":{"crumb":"9q.A4D1c.b9
        for l in lines:
            if re.findall(r'CrumbStore', l):
                return l

    def split_crumb_store(self, v):
        return v.split(':')[2].strip('"')

    def get_cookie_crumb(self, symbol):
        cookie, lines = self.get_page_data(symbol)
        crumb = self.split_crumb_store(self.find_crumb_store(lines))
        return cookie, crumb

    def string2ts(self, string, fmt="%Y-%m-%d"):
        dt = datetime.datetime.strptime(string, fmt)
        t_tuple = dt.timetuple()
        return int(time.mktime(t_tuple))

    def get_k_data(self, code, start_date, end_date):
        try:
            start_date = self.string2ts(start_date)
            end_date = self.string2ts(end_date)

            cookie, crumb = self.get_cookie_crumb(code)

            url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events" \
                  "=history&crumb=%s" % (
                      code, start_date, end_date, crumb)

            logger.debug(url)
            response = requests.get(url, cookies=cookie)

            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            df["code"] = code
            df = df.drop(columns=['Adj Close'])
            df = df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high',
                                    'Low': 'low', 'Close': 'close', 'Volume': 'volume'})

            df['pre_close'] = df['close'].shift(1)
            df = df.dropna()
            return df
        except Exception as e:
            logger.error(repr(e))
            raise e

    @exc_time
    def get_real_price(self, code):
        url = "https://finance.yahoo.com/quote/%s/?p=%s" % (code, code)
        r = requests.get(url)
        selector = etree.HTML(r.text)
        price_el = selector.xpath('//div/span/text()')
        price = float(price_el[1].replace(',',''))
        pre_close_el = selector.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span/text()')
        pre_close = float(pre_close_el[0].replace(',',''))

        return price, pre_close


yahoo_finance_api = YahooFinanceApi()

