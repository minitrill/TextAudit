#!/usr/bin/env python
# encoding:utf-8


"""
使用贝叶斯模型进行文本分类


author    :   @h-j-13
time      :   2018-7-21
ref       :   https://blog.csdn.net/github_36326955/article/details/54891204
"""

import sys
import cPickle as pickle

from sklearn import metrics
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法

TF_IDF_PATH = './data/WordBag/if_idf.txt'

reload(sys)
sys.setdefaultencoding('utf-8')

TF_IDF_PATH = './data/WordBag/if_idf.txt'


# 读取bunch对象
def read_obj(path):
    with open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch


# 导入训练集
TRAIN_SET = read_obj(TF_IDF_PATH)

# 训练分类器：输入词袋向量和分类标签，alpha:0.001 alpha越小，迭代次数越多，精度越高

# KNN
# clf = KNeighborsClassifier()

# 决策树
clf = tree.DecisionTreeClassifier()
clf.fit(TRAIN_SET.tdm, TRAIN_SET.label)
# clf = MultinomialNB(alpha=0.001).fit(TRAIN_SET.tdm, TRAIN_SET.label)

# 预测分类结果
predicted = clf.predict(TRAIN_SET.tdm)

for flabel, file_name, expct_cate in zip(TRAIN_SET.label, TRAIN_SET.filenames, predicted):
    if flabel != expct_cate:
        print file_name, ": 实际类别:", flabel, " -->预测类别:", expct_cate

print "预测完毕!!!"

# 计算分类精度：
from sklearn import metrics


def metrics_result(actual, predict):
    print '精度:{0:.3f}'.format(metrics.precision_score(actual, predict, average='weighted'))
    print '召回:{0:0.3f}'.format(metrics.recall_score(actual, predict, average='weighted'))
    print 'f1-score:{0:.3f}'.format(metrics.f1_score(actual, predict, average='weighted'))


metrics_result(TRAIN_SET.label, predicted)
