#!/usr/bin/env python
# encoding:utf-8

"""
gensim 库简单学习使用

author    :   @h-j-13
time      :   2018-7-23
"""

import logging
import warnings

warnings.filterwarnings(action='ignore')

import numpy as np
from gensim.models import word2vec, KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

raw_sentences = ["the quick brown fox jumps over the lazy dogs",
                 "yoyoyo you go home now to sleep"]

sentences = [s.encode('utf-8').split() for s in raw_sentences]

# 构建模型
model = word2vec.Word2Vec(sentences, min_count=1)
# Word2Vec 参数

# 1. min_count : 在不同大小的语料集中，我们对于基准词频的需求也是不一样的。譬如在较大的语料集中，我们希望忽略那些只出现过一两次的单词，
# 这里我们就可以通过设置min_count参数进行控制。一般而言，合理的参数值会设置在0~100之间。

# 2. size : 主要是用来设置神经网络的层数，Word2Vec 中的默认值是设置为100层。
# 更大的层次设置意味着更多的输入数据，不过也能提升整体的准确度，合理的设置范围为 10~数百。

# 3. workers 参数用于设置并发训练时候的线程数，不过仅当Cython安装的情况下才会起作用(默认值为1,不进行并发)

# word2vec
print model['the']  # 将词转化为100个向量的矩阵
# 进行相关性比较
print model.similarity('dogs', 'you')  # -0.037060834
# 最相似的词
print model.most_similar(['you'])

# # 模型的保存与读取
# model.save('test.model')
# model1 = word2vec.Word2Vec.load('test.model')
#
# # 二进制方式
# model.wv.save_word2vec_format('test.model.bin', binary=True)
# model2 = KeyedVectors.load_word2vec_format('test.model.bin', binary=True)
