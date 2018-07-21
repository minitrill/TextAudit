#!/usr/bin/env python
# encoding:utf-8


"""
停用词处理
整合多个停用词文本,生成停用词字典,并支持更新并保存到文件中

>>> stop_words = get_stop_words()

stop_words  # ...set(['stop word1', 'stop word1' ,...])

author    :   @h-j-13
time      :   2018-7-18
"""

import os


def converge_files_data(files=[]):
    """聚合文件中的敏感词信息"""
    stop_words_set = set()
    for file in files:
        with open(file, 'rb') as f:
            for word in f:
                if not word.startswith('//'):
                    stop_words_set.add(word.strip())
    # 处理空字符串
    if '' in stop_words_set:
        stop_words_set.remove('')

    return stop_words_set


def record_stop_words_data(stop_words, file_path='./data/stop_words.txt'):
    """记录停用词到日志中"""
    with open(file_path, 'wb') as f:
        for words in stop_words:
            print words
            f.write(words)
            f.write("\n")


def get_stop_words(file_path='./data/stop_words.txt'):
    """获取停用词列表"""
    stop_words_set = set()
    with open(file_path, 'rb') as f:
        for word in f:
            if not word.startswith('//'):
                stop_words_set.add(word.strip().decode('utf8'))
    # 处理空字符串
    if '' in stop_words_set:
        stop_words_set.remove('')

    return stop_words_set
