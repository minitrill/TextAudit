#!/usr/bin/env python
# encoding:utf-8


"""
jieba分词学习及测试

author    :   @h-j-13
time      :   2018-7-18
"""

# note
# 精确模式，试图将句子最精确地切开，适合文本分析；
# 全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
# 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。

import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))          # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))       # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")          # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))

seg_list = jieba.cut("430的祈求者玩的非常好")
print(", ".join(seg_list))
jieba.add_word('祈求者', freq=None, tag=None)
seg_list = jieba.cut("430的祈求者玩的非常好")
print(", ".join(seg_list))