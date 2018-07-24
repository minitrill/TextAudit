#!/usr/bin/env python
# encoding:utf-8


"""
敏感词处理
从文件中读取敏感词,添加不同类别的敏感词,保存到txt或者DB中

# >>>s = SensitiveWords()
# >>>s.get_sensitive_word('./data/SensitiveWords/ad.txt') # 读取文件中的敏感词,要求数据每个一行
# >>>s.add_sensitive_word(u'default')                     # 添加敏感词 unicode
# >>>s.add_sensitive_word('minitrill', word_type='ad')    # 添加敏感词 str 并指定敏感词类型
# >>>s.save_data()                                        # 保存敏感词数据
# >>>s.sensitive_word_dict                                # 核心数据被保存在字典中

author    :   @h-j-13
time      :   2018-7-19
"""

import os

SENSITIVE_WORDS_DATA_PATH = "./data/SensitiveWords/"  # 敏感词数据文件(要求一类数据一个txt文件)
SENSITIVE_WORDS_DEFAULT_WEIGHT = {
    "ad": 10,
    "default": 10,
    "dirty": 5,
    "illegal": 30,
    "pron": 20,
    "politics": 35,
}


class SensitiveWords(object):
    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(SensitiveWords, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        """构造函数:读取敏感词文件并初始化字典"""
        global SENSITIVE_WORDS_DATA_PATH
        self.file_name_list = os.listdir(SENSITIVE_WORDS_DATA_PATH)
        self.file_path_list = map(lambda s: SENSITIVE_WORDS_DATA_PATH + s, self.file_name_list)
        self.sensitive_word_dict = {}
        for file_path in self.file_path_list:
            self.get_sensitive_word(file_path)

    def get_sensitive_word(self, path):
        """从文件中读取敏感词"""
        global SENSITIVE_WORDS_DEFAULT_WEIGHT
        with open(path, 'rb') as f:
            sensitive_word_type = str(path).split('/')[-1].replace('.txt', '')
            self.sensitive_word_dict[sensitive_word_type] = {}
            for line in f:
                if sensitive_word_type == 'illegal':
                    print line
                if line.strip():
                    line_stplit = line.strip().split('\t')
                    if len(line_stplit) == 2:
                        word, weight = line_stplit
                        word = word.strip().decode('utf-8')
                        weight = float(weight)
                    else:
                        word = line.strip().decode('utf-8')
                        weight = SENSITIVE_WORDS_DEFAULT_WEIGHT[sensitive_word_type]
                    self.sensitive_word_dict[sensitive_word_type][word] = weight

    def add_sensitive_word(self, word, word_type='default', word_weight='10'):
        """添加敏感词"""
        if type(word) == str:  # str -> unicode
            word = word.decode('utf-8')
        if word_type in self.sensitive_word_dict.keys() or word_type == 'default':
            self.sensitive_word_dict[word_type][word] = word_weight

    def save_data(self):
        """存储数据到文件中"""
        for word_type in self.sensitive_word_dict.keys():
            file_path = filter(lambda x: word_type in x, self.file_path_list)[0]
            with open(file_path, 'wb') as f:
                for word, weight in self.sensitive_word_dict[word_type].items():
                    f.write(word.encode("utf-8"))
                    f.write("\t")
                    f.write(str(weight))
                    f.write("\n")


if __name__ == '__main__':
    SensitiveWords().get_sensitive_word("./data/SensitiveWords/illegal.txt")
    # for i,v in SensitiveWords().sensitive_word_dict.items():
    #     print i
