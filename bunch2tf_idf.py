#!/usr/bin/env python
# encoding:utf-8


"""
bunch模型转化为TF-IDF空间向量


author    :   @h-j-13
time      :   2018-7-21
ref       :   https://blog.csdn.net/github_36326955/article/details/54891204
"""

import sys
import cPickle as pickle

from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer

from stop_words import get_stop_words

reload(sys)
sys.setdefaultencoding('utf-8')

BUNCH_PATH = './data/WordBag/bunch.txt'
TF_IDF_PATH = './data/WordBag/if_idf.txt'


# 读写对象
def read_obj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


def write_obj(path, bunchobj):
    with open(path, "wb") as file_obj:
        pickle.dump(bunchobj, file_obj)


def vector_space():
    """创建TF-IDF词向量空间"""
    stop_words_list = list(get_stop_words())
    bunch = read_obj(BUNCH_PATH)  # 导入分词后的词向量bunch对象
    # 构建tf-idf词向量空间对象
    tfidfspace = Bunch(target_name=bunch.target_name,
                       label=bunch.label,
                       filenames=bunch.filenames,
                       tdm=[],
                       vocabulary={})

    # 使用TfidfVectorizer初始化向量空间模型
    # 这里面有TF-IDF权重矩阵还有我们要的词向量空间坐标轴信息vocabulary_
    vectorizer = TfidfVectorizer(stop_words=stop_words_list, sublinear_tf=True, max_df=0.5)
    # 此时tdm里面存储的就是if-idf权值矩阵
    tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
    tfidfspace.vocabulary = vectorizer.vocabulary_
    # 结果写入文件
    write_obj(TF_IDF_PATH, tfidfspace)
    print "if-idf词向量空间实例创建成功！"


if __name__ == '__main__':
    vector_space()