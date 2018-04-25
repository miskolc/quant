#!/usr/bin/python
# -*- coding: utf-8 -*-

# engine.py


from app.dao import price_retrieval

# 中证500成份股, 股票价格获取
if __name__ == "__main__":
    # 当前时间
    # now = datetime.now()
    # 前一天
    # pre = now - timedelta(days=1)
    # format date to string
    # start = pre.strftime('%Y-%m-%d')
    # end = now.strftime('%Y-%m-%d')
    # print('start=%s,end=%s' % (start, end))

    #df = ts.get_zz500s()
    price_retrieval.price_retrieval_daily('000725', '2015-01-23', '2018-04-23')
    #sz500_codes = df["code"].values;
    #for code in sz500_codes:
        #price_retrieval.price_retrieval_daily(code, '2018-04-23', '2018-04-23')

        # price_retrieval.price_retrieval_daily('sh', '2015-01-01', start)
