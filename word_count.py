#!/usr/bin/env python
# encoding:utf-8

"""
词频统计

author    :   @h-j-13
time      :   2018-7-31
"""

import nltk
import jieba
from collections import Counter

from stop_words import get_stop_words

malicious_data_url = './data/minitrill/malicious_text.txt'
normal_data_url = './data/minitrill/normal_text.txt'


class WordCount(object):
    """词频及其他信息统计"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.stop_words = get_stop_words()
        self.text = []
        self.text_analysis = {}
        self.word_count_dict = {}
        self.add_user_dict()

    def add_user_dict(self):
        """针对结巴分词加载自定义词典"""
        jieba.add_word("法轮大法")
        # add malicious word...

    def read_file(self):
        """读取文件内容"""
        with open(self.file_path, 'rb') as f:
            for line in f:
                self.text.append(line.decode('utf8').strip())
        print "读取文本完毕 - 共" + str(len(self.text)) + "行"

    def analysis_text(self):
        """分析文本数据"""
        for t in self.text:
            temp = t.split(u'-')
            t_type = temp[0]
            t_text = temp[1]
            if self.text_analysis.has_key(t_type):
                self.text_analysis[t_type].append(t_text)
            else:
                self.text_analysis[t_type] = [t_text]

        print "文本分析结果:"
        for k in self.text_analysis.keys():
            print str(k) + " 类 - 文本数量 " + str(len(self.text_analysis[k]))

    def word_count(self, top_n=50):
        """分词后统计词频"""
        for k in self.text_analysis.keys():
            self.word_count_dict[k] = []
            temp = []
            for text in self.text_analysis[k]:
                # 分词后去除停用词
                temp.extend(list(set(jieba.cut(text, cut_all=True)) - set(self.stop_words)))
            d = dict(Counter(temp))
            d = sorted(d.items(), key=lambda x: x[1], reverse=True)
            for x in d[:top_n]:
                if x[0]:

                    self.word_count_dict[k].append(x[0])

    def save_word_count_dict(self):
        """保存分词之后的数据"""
        for k in self.word_count_dict.keys():
            with open(str(k) + ".txt", "wb") as f:
                for t in self.word_count_dict[k]:
                    f.write(str(t.encode('utf8')) + "\n")


if __name__ == '__main__':
    w = WordCount(malicious_data_url)
    w.read_file()
    w.analysis_text()
    w.word_count()
    w.save_word_count_dict()
