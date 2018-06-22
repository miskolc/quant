# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import requests
from lxml import etree
import pandas as pd

from quant.common_tools.decorators import exc_time


class SinaFinanceApi:
    @exc_time
    def get_stock_structure_by_code(self, code):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/%s.phtml" % (code)
        r = requests.get(url, headers=headers)

        try:
            selector = etree.HTML(r.content.decode('gb2312'))
        except Exception:
            return None

        df = pd.DataFrame(columns=['code', 'name', 'date', 'share_oustanding'])
        #// *[ @ id = "StockStructureNewTable1"] / tbody / tr[1] / td[2]

        for j in range(0, 4):

            for i in range(2, 7):
                try:
                    name = selector.xpath('//*[@id="toolbar"]/div[1]/h1/a/text()')[0]
                    date = selector.xpath('//*[@id="StockStructureNewTable%s"]/tbody/tr[1]/td[%s]/text()' % (j,i))[0]

                    if date is None:
                        continue

                    share_oustanding = selector.xpath('//*[@id="StockStructureNewTable%s"]/tbody/tr[7]/td[%s]/text()' % (j,i))[0]
                    share_oustanding = share_oustanding.split(' ')[0]

                    if share_oustanding == '--':
                        continue

                    df = df.append({'code': code, 'name': name, 'date': date, 'share_oustanding': share_oustanding}, ignore_index=True)
                except Exception:
                    pass

        return df

sina_finance_api = SinaFinanceApi()

