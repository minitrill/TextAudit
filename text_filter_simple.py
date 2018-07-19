#!/usr/bin/env python
# encoding:utf-8


"""
文本过滤器
使用python内建的 in,replace 实现文本过滤


author    :   @h-j-13
time      :   2018-7-19
"""

from sensitive_word import SensitiveWords

senstive_data_list = []


def init_data():
    global senstive_data_list
    temp = SensitiveWords().sensitive_word_dict
    data = []
    for k in temp.keys():
        data.extend(list(temp[k]))
    senstive_data_list = data


def text_filter(s):
    """文本过滤"""
    global senstive_data_list
    data = senstive_data_list

    if type(s) == str:
        s = s.decode('utf-8')

    for word in data:
        if word in s:
            s = s.replace(word, u'*')
    return s


if __name__ == '__main__':
    init_data()
    print text_filter(u'ABC')
    print text_filter(u'人妻')
