#!/usr/bin/env python
# encoding:utf-8


"""
通过jieba分词对文本文件数据进行分词并保存到文件中

author    :   @h-j-13
time      :   2018-7-20
"""

import os
import sys
import jieba

reload(sys)
sys.setdefaultencoding('utf8')

train_data_url = './data/FudanTrainData/'
segment_data_url = './data/WordSegment/'

from stop_words import get_stop_words

STOP_WORDS_SET = get_stop_words()


def get_all_file_by_path(path=train_data_url):
    """获取某个目录下的所有训练文件"""
    file_path = []
    dir_list = os.listdir(train_data_url)
    for d in dir_list:
        file_path.extend(map(lambda x: train_data_url + d + '/' + x, os.listdir(train_data_url + d)))
    return file_path


def read_file_sentence(file_path='./data/FudanTrainData/C3-Art/C3-Art0002.txt'):
    """读取文件,将全文转化为句子并进行分词,然后去除停用词,返回分词之后的结果 'w1 w2 w3'"""

    with open(file_path, 'rb') as f:
        content = f.read().encode('utf8')

    content = content.replace("\r\n", "")  # 删除换行
    content = content.replace(" ", "")  # 删除空行、多余的空格
    content_seg = jieba.cut(content)  # 为文件内容分词,注意分词之后是unicode
    content_seg_list = [word for word in content_seg]  # jieba默认返回一个迭代器,转化为list
    content_seg_without_stopwords = list(set(content_seg_list) - STOP_WORDS_SET)  # 去除停用词
    content_seg_without_stopwords.sort(key=content_seg_list.index)  # 按原列表排序

    return u" ".join(content_seg_without_stopwords).encode('utf8')


if __name__ == '__main__':
    old_data_type = ''

    for file_path in get_all_file_by_path():
        [data_type, file_name] = file_path.split('/')[-2:]

        res = read_file_sentence(file_path)

        if old_data_type != data_type:
            os.makedirs(segment_data_url + data_type)
            old_data_type = data_type

        with open(segment_data_url + data_type + '/' + file_name, 'wb') as f:
            f.write(res)
