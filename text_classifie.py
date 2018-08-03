#!/usr/bin/env python
# encoding:utf-8


"""
文本分类模型
基于TF-IDF结合多种算法的文本分类器模型

>>>t = TextClassifie()          # 初始化
>>>t.set_classifie_model()      # 选择分类器模型
>>>t.init_clf()                 # 分类器初始化

>>>d = DataSet()        # 构建数据集
>>>d.set_labels(["人", "物"])                        # 设置标签
>>>d.add_data("我叫jerry", 'train_data_1', data_labels='人')  # 添加数据(文本,id,标签)
>>>d.add_data("这个是桌子", 'train_data_2', data_labels='物体')
>>>tarin_data = d.train2tf_idf()                         # 生成tf-idf数据
>>>train_data.save_tf_idf_data()                         # 保存数据到文件中
>>>train_data.read_tf_idf_data()                         # 从文件中读取数据

>>>t.train(tarin_data)                                   # 训练模型
>>>t.predicted(tarin_data)                               # 对数据进行文本分类(这里用训练数据代替,用同样的方式可以生成测试数据
>>># ['人','物体']
>>>t.metrics_result()
>>># 比对模型精度(只针对打好标签的训练集)

author    :   @h-j-13
time      :   2018-7-21
"""

import os
import sys
import time
import warnings
import cPickle as pickle

import jieba
import numpy as np

# data moudle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics

# classifie
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from stop_words import get_stop_words
from sensitive_word import SensitiveWords

reload(sys)
sys.setdefaultencoding('utf-8')

warnings.filterwarnings("ignore")

# 文本训练模型编号
CLASSIFIE_SVM = 0
CLASSIFIE_MultinomialNB = 1
CLASSIFIE_DecisionTree = 2
CLASSIFIE_LogisticRegression = 3
CLASSIFIE_RandomForest = 4
CLASSIFIE_KNN = 5
CLASSIFIE_GBDT = 6

train_data_tf_idf_path = ""
test_data_tf_idf_path = ""

TfidfVectorizer_OBJ = None
TfidfVectorizer_init = False
ADD_USER_DICT = False


class DataSet(object):
    """用于文本分类的数据集,可以通过这个训练数据集和测试集,适用于sklearn框架"""

    def __init__(self):
        """构造函数"""
        global TfidfVectorizer_OBJ
        self.bunch = Bunch(label_set=[],  # 分类类别(去重过)
                           labels=[],  # 每条数据的分类
                           ids=[],  # 每条数据的唯一id
                           contents=[])  # 每条数据经过预处理,分词之后的内容
        self.stop_words = list(get_stop_words())
        self.has_tf_idf = False  # 是否生成了tf_idf向量空间数据
        self.tf_idf_vector_space = None
        # 全局只是使用一个tf-idf量化器
        if TfidfVectorizer_OBJ is None:
            TfidfVectorizer_OBJ = TfidfVectorizer(stop_words=self.stop_words, sublinear_tf=True, max_df=0.5)
        self.tf_idfVectorizer = TfidfVectorizer_OBJ
        self.add_user_dict()

    def __str__(self):
        """支持print方法输出数据集信息"""
        res = "目前数据集共有 " + str(len(self.bunch.label_set)) + " 种类型数据 :\n " + " | ".join(self.bunch.label_set) + "\n" \
              + "共计 " + str(len(self.bunch.contents)) + " 条文本数据"
        return res

    def __len__(self):
        """使用文本数量来表示数据集数量"""
        return len(self.bunch.contents)

    def size(self):
        """获取数据集大小"""
        return {"label num": len(set(self.bunch.label_set)),
                "data num": len(self.bunch.contents)}

    def add_user_dict(self):
        """添加已知的敏感词作为用户词典"""
        global ADD_USER_DICT
        if not ADD_USER_DICT:  # 全局只用添加一次就够了
            ADD_USER_DICT = True
            sw = SensitiveWords()
            for k in sw.sensitive_word_dict.keys():
                for word in sw.sensitive_word_dict[k]:
                    jieba.add_word(word)

    def set_labels(self, label_list):
        """设置数据集的分类标签"""
        self.bunch.label_set = list(set(label_list))
        self.bunch.label_set.append(u"default")  # 增加一个默认类别,用于存放训练数据

    def add_data(self, data, data_id, data_labels=u"default"):
        """向数据集中添加数据,必须确定数据id及内容(要求输入字符串是utf8格式)"""
        self.bunch.labels.append(data_labels)
        self.bunch.ids.append(data_id)
        content = data
        content.replace(u"\r\n", u"")  # 删除换行
        content.replace(u"\t", u"")  # 删除制表符
        content = content.replace(u" ", u"")  # 删除空行、多余的空格
        content_seg = jieba.cut(content)  # 为文件内容分词,注意分词之后是unicode
        content_seg_list = [word for word in content_seg]  # jieba默认返回一个迭代器,转化为list
        self.bunch.contents.append(" ".join(content_seg_list))

    def train2tf_idf(self):
        """将数据转换为TF-IDF向量空间数据"""
        # 构建tf-idf词向量空间对象
        tfidfspace = Bunch(labels_set=self.bunch.label_set,
                           labels=self.bunch.labels,
                           ids=self.bunch.ids,
                           tdm=[],
                           vocabulary={})
        # 使用TfidfVectorizer初始化向量空间模型
        # tfidfspace.tdm = self.tf_idfVectorizer.fit_transform(self.bunch.contents)

        # 处理一个坑
        # ref - https://stackoverflow.com/questions/45804133/dimension-mismatch-error-in-countvectorizer-multinomialnb
        # ref - https://cuiqingcai.com/4759.html
        # 只有第一次用 fit_transform() 其他的时候量化器只要 transform() 就可以了

        # 生成tf_idf数据对象
        global TfidfVectorizer_init
        if not TfidfVectorizer_init:
            tfidfspace.tdm = self.tf_idfVectorizer.fit_transform(self.bunch.contents)
            TfidfVectorizer_init = True
        else:
            tfidfspace.tdm = self.tf_idfVectorizer.transform(self.bunch.contents)
        tfidfspace.vocabulary = self.tf_idfVectorizer.vocabulary_

        self.has_tf_idf = True
        self.tf_idf_vector_space = tfidfspace
        return tfidfspace

    def save_tf_idf_data(self, tf_idf_data_path="./data/tf_idf.dat"):
        """保存向量空间数据到文件中(基于pickle)"""
        if self.has_tf_idf:
            with open(tf_idf_data_path, "wb") as file_obj:
                pickle.dump(self.tf_idf_vector_space, file_obj)
        else:
            raise Exception("尚未生成if-idf数据,请生成后再执行保存操作")

    def read_tf_idf_data(self, tf_idf_data_path="./data/tf_idf.dat"):
        """将文件中的if-idf数据读取到本地"""
        with open(tf_idf_data_path, "rb") as file_obj:
            data = pickle.load(file_obj)
        self.has_tf_idf = True
        self.tf_idf_vector_space = data
        return self.tf_idf_vector_space


class TextClassifie(object):
    """文本分类器,支持多种模型进行分类,基于tf-idf数据"""

    def __init__(self):
        self.clf = None
        self.clf_num = 1
        self.bayes_alpha = 0.001
        self.train_data = None
        self.test_data = None
        self.predicted_data = None
        self.kNN_neighbors = None

    def set_classifie_model(self, model_num=1):
        """选择文本分类模型"""
        self.clf_num = model_num

    def set_bayes_alpha(self, val):
        """设置贝叶斯的alpha值"""
        self.bayes_alpha = val

    def set_kNN_neighbors(self, val):
        """设置KNN分类器聚类个数"""
        self.kNN_neighbors = val

    def init_clf(self):
        """构建分类模型"""
        if self.clf_num == 0:
            self.clf = svm.SVC()
            print "使用支持向量机分类模型(SVM)"
        elif self.clf_num == 1:
            print "使用alpha=" + str(self.bayes_alpha) + "的多项式贝叶斯分类模型"
            self.clf = MultinomialNB(alpha=self.bayes_alpha)
        elif self.clf_num == 2:
            print "使用决策树分类模型"
            self.clf = DecisionTreeClassifier()
        elif self.clf_num == 3:
            print "使用逻辑回归分类模型"
            self.clf = LogisticRegression()
        elif self.clf_num == 4:
            print "使用随机森林分类模型"
            self.clf = RandomForestClassifier()
        elif self.clf_num == 5:
            print "使用kNN聚类模型"
            self.clf = KNeighborsClassifier(self.kNN_neighbors)
        elif self.clf_num == 6:
            print "使用GBDT聚类模型"
            self.clf = GradientBoostingClassifier()

    def train(self, train_data):
        """训练文本分类模型"""
        self.train_data = train_data
        start_time = time.time()
        self.clf.fit(train_data.tdm, train_data.labels)
        print "训练所用时间 : {0:.4f} sec".format(time.time() - start_time)

    def predicted(self, test_data):
        """进行文本分类"""
        self.test_data = test_data
        start_time = time.time()
        self.predicted_data = self.clf.predict(test_data.tdm)
        print "分类所用时间 : {0:.4f} sec".format(time.time() - start_time)
        return self.predicted_data

    def metrics_result(self):
        """对测试集合进行比较"""
        print '精度:{0:.5f}'.format(
            metrics.precision_score(self.test_data.labels, self.predicted_data, average='weighted'))
        print '召回:{0:.5f}'.format(metrics.recall_score(self.test_data.labels, self.predicted_data, average='weighted'))
        print 'f1-score:{0:.5f}'.format(
            metrics.f1_score(self.test_data.labels, self.predicted_data, average='weighted'))


if __name__ == '__main__':
    # ===========================文本分类模型================================
    train_data = DataSet()
    test_data = DataSet()

    train_data.read_tf_idf_data("./data/train.dat")
    test_data.read_tf_idf_data("./data/test.dat")

    t = TextClassifie()
    t.set_classifie_model()
    # t.set_bayes_alpha(0.0001)
    t.init_clf()

    t.train(train_data.tf_idf_vector_space)
    t.predicted(test_data.tf_idf_vector_space)

    t.metrics_result()

    # --------------------- RESULT ------------------------
    # 使用alpha=0.0001的多项式贝叶斯分类模型
    # 训练所用时间 : 0.3540 sec
    # 分类所用时间 : 0.0060 sec
    # 精度:0.96798
    # 召回:0.96962
    # f1-score:0.96301

    # after add user dict
    # 使用alpha=0.001的多项式贝叶斯分类模型
    # 训练所用时间 : 0.3670 sec
    # 分类所用时间 : 0.0080 sec
    # 精度:0.96878
    # 召回:0.97030
    # f1-score:0.96409

    # 正负 1:5
    # 使用alpha=0.001的多项式贝叶斯分类模型
    # 训练所用时间 : 0.0920 sec
    # 分类所用时间 : 0.0020 sec
    # 精度:0.90207
    # 召回:0.90250
    # f1-score:0.88676

    # ==========================生成测试数据==========================
    # malicious_data_url = './data/minitrill/malicious_text.txt'
    # normal_data_url = './data/minitrill/normal_text_s.txt'
    #
    # p = 0
    # id_count = 0
    # # dataset init
    # train_data = DataSet()
    # test_data = DataSet()
    #
    # train_data.set_labels(["0", "20001", "20002", "20004", "20006"])
    # test_data.set_labels(["0", "20001", "20002", "20004", "20006"])
    # # read file
    # with open(malicious_data_url, "rb") as f:
    #     for line in f:
    #         l = line.decode('utf8').strip()
    #         x = l.split('-', 1)
    #         if p > 4: # 4:1 train/test
    #             p = 0
    #             test_data.add_data(x[1], str(id_count), data_labels=x[0])
    #         else:
    #             train_data.add_data(x[1], str(id_count), data_labels=x[0])
    #
    #         id_count += 1
    #         p += 1
    # with open(normal_data_url, "rb") as f:
    #     for line in f:
    #         l = line.decode('utf8').strip()
    #         x = l.split('-', 1)
    #         if p > 8:
    #             p = 0
    #             test_data.add_data(x[1], str(id_count), data_labels=x[0])
    #         else:
    #             train_data.add_data(x[1], str(id_count), data_labels=x[0])
    #
    #         id_count += 1
    #         p += 1
    #
    # # tf-idf
    # train_data.train2tf_idf()
    # test_data.train2tf_idf()
    # # save
    # train_data.save_tf_idf_data("./data/train.dat")
    # test_data.save_tf_idf_data("./data/test.dat")

    # ==========================构造测试文本 5 -> 1=====================
    # malicious_data_url = './data/minitrill/malicious.txt'
    # normal_data_url = './data/minitrill/normal.txt'
    #
    # count = 0
    # fr = open('./data/minitrill/normal_text_s.txt', 'wb')
    # with open(normal_data_url, 'rb') as f:
    #     for line in f:
    #         line = line.decode('utf8').strip()
    #         t = line.split('\t')
    #         count += 1
    #         if count >= 4:
    #             fr.write(str(t[0]) + '-' + str(t[-1]) + '\n')
    #             count = 0