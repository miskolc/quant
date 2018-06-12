# coding=utf-8
# ae_h - 2018/6/11

import nltk
import tushare as ts
import jieba.posseg as pseg
import jieba
import re
import pandas as pd
from nltk.corpus import stopwords
from collections import OrderedDict


def muning_tushare_new():
    instant_news_df = ts.get_latest_news(show_content=True)
    sina_new_df = ts.guba_sina(show_content=True)
    instant_titles = instant_news_df['title']
    instant_content = instant_news_df['content']

    sina_titles = sina_new_df['title']
    sina_content = sina_new_df['content']

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

    news_collection = instant_title_str + instant_content_str + sina_title_str + sina_content_str

    return news_collection


def word_analysis(args):
    # stops_words = set(stopwords.words("english"))

    stops_words = []
    jieba.load_userdict('/Users/yw.h/quant-awesome/quant/collector/news_nlp/custome_word.txt')

    with open('/Users/yw.h/quant-awesome/quant/collector/news_nlp/stop_word.txt', 'rb') as f:
        for line in f:
            line = line.decode('utf-8').strip('\n')
            stops_words.append(line)

    w_list = jieba.cut(args)

    # w_list = []

    # words = pseg.cut(args)

    # print(words)
    #
    # print(type(words))
    #
    # for keys in words:
    #     w_list.append(keys.word)
    #
    # print(w_list)

    # print(stops_words)
    #
    # print(w_list)
    filtered_words = []

    for word in w_list:
        if word not in stops_words:
            filtered_words.append(word)
        else:
            pass

    freq_result = nltk.FreqDist(filtered_words)

    freq_dict = {}

    for i in freq_result:
        if i in [' ', '\n', 'c', '\t', 'px', '%', '{', '}', '\xa0', '_'] or re.match(r'^\d{n}$', i) or re.match(r'^(-?\d+)(\.\d+)?$', i) or re.match(r'[\d.]+%', i):
            pass
        else:
            freq_dict[i] = freq_result[i]

    freq_dict = sorted(freq_dict.items(), key=lambda t: t[1], reverse=True)
    print(freq_dict)


if __name__ == '__main__':
    sth = muning_tushare_new()
    word_analysis(sth)
