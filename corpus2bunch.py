#!/usr/bin/env python
# encoding:utf-8


"""
文集处理为Bunch


author    :   @h-j-13
time      :   2018-7-20
"""

import os
import sys
import cPickle as pickle  # cPickle可以对任意一种类型的python对象进行序列化操作

from sklearn.datasets.base import Bunch


reload(sys)
sys.setdefaultencoding('utf-8')

WORD_SEGMENT_PATH = './data/WordSegment/'
WORD_BAG_PATH = './data/WordBag/bunch.txt'


def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'rb') as f:
        contents = f.read()
    return contents


def corpus2Bunch(word_bag_path=WORD_BAG_PATH, word_segment_path=WORD_SEGMENT_PATH):
    """将文本转化为Bunch模型"""
    # 创建一个Bunch实例
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    class_list = os.listdir(word_segment_path)
    bunch.target_name.extend(os.listdir(word_segment_path))
    # 处理每个分类下的所有文件
    for class_name in class_list:
        class_path = word_segment_path + class_name + "/"  # 拼出分类子目录的路径
        # 构建Bunch
        for file_name in os.listdir(class_path):  # 遍历类别目录下文件
            file_path = class_path + '/' + file_name
            bunch.label.append(class_name)
            bunch.filenames.append(file_path)
            bunch.contents.append(read_file(file_path))  # 读取文件内容

    # 将bunch存储到wordbag_path路径中
    with open(word_bag_path, "wb") as f:
        pickle.dump(bunch, f)
    print "构建文本对象Bunch结束！"


if __name__ == '__main__':
    corpus2Bunch()
