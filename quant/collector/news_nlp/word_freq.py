# coding=utf-8
# ae_h - 2018/6/11

import nltk
import tushare as ts

instant_news_df = ts.get_latest_news(show_content=True)
sina_new_df = ts.guba_sina(show_content=True)


instant_titles = instant_news_df['title']
instant_content = instant_news_df['content']

sina_titles = sina_new_df['title']
sina_content = sina_new_df['content']


def word_an

instant_title_str = ''
for i_t in instant_titles:
    if i_t is None:
        it = ''
    instant_title_str = instant_title_str + i_t

instant_content_str = ''
for i_c in instant_content:
    if i_c is None:
        i_c = ''
    instant_content_str = instant_content_str + i_c

sina_title_str = ''
for s_t in sina_titles:
    if s_t is None:
        s_t = ''
    sina_title_str = sina_title_str + s_t

sina_content_str = ''
for s_c in sina_content:
    if s_c is None:
        s_c = ''
    sina_content_str = sina_content_str + s_c

new_collection = instant_title_str + instant_content_str + sina_title_str + sina_content_str
print(new_collection)





