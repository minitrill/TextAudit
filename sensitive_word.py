#!/usr/bin/env python
# encoding:utf-8


"""
敏感词处理
从文件中读取敏感词,添加不同类别的敏感词,保存到txt或者DB中

author    :   @h-j-13
time      :   2018-7-19
"""


class SensitiveWords(object):
    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(SensitiveWords, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.file_path_list = ['./data/SensitiveWords/ad.txt',
                               './data/SensitiveWords/dirty.txt',
                               './data/SensitiveWords/gun.txt',
                               './data/SensitiveWords/politics.txt',
                               './data/SensitiveWords/pron.txt',
                               './data/SensitiveWords/default.txt']
        self.sensitive_word_dict = {}
        for file in self.file_path_list:
            self.get_sensitive_word(file)

    def get_sensitive_word(self, path):
        """从文件中读取敏感词"""
        with open(path, 'rb') as f:
            sensitive_word_type = str(path).split('/')[-1].replace('.txt', '')
            self.sensitive_word_dict[sensitive_word_type] = set()
            for line in f:
                if line.strip():
                    self.sensitive_word_dict[sensitive_word_type].add(line.strip())

    def add_sensitive_word(self, word, word_type='default'):
        """添加敏感词"""
        if word_type in self.sensitive_word_dict.keys() or word_type == 'default':
            self.sensitive_word_dict[word_type].add(word)

    def save_data(self):
        """存储数据到文件中"""
        for word_type in self.sensitive_word_dict.keys():
            file_path = filter(lambda x: word_type in x, self.file_path_list)[0]
            with open(file_path, 'wb') as f:
                for word in self.sensitive_word_dict[word_type]:
                    f.write(word)
                    f.write("\n")


if __name__ == '__main__':
    s = SensitiveWords()
    s.get_sensitive_word('./data/SensitiveWords/ad.txt')
    s.add_sensitive_word('test')
    s.add_sensitive_word('迷药', 'ad')
    s.save_data()
