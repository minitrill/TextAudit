#!/usr/bin/env python
# encoding:utf-8


"""
base64编解码处理
用于处理某些被加密的敏感词库

author    :   @h-j-13
time      :   2018-7-18
"""

import os
import base64


def decode64file(path_file):
    """解码base64加密的文件"""
    with open(path_file, 'rb') as f:
        str_set = set()
        for line in f:
            s = line.strip()
            if s.endswith('Cg=='):
                s = s.replace('Cg==', '')
            str_set.add(base64.b64decode(s))

    return str_set


train_data_url = './data/FudanTrainData/'


def get_all_file_by_path(path=train_data_url):
    """获取某个目录下的所有训练文件"""
    file_path = []
    dir_list = os.listdir(train_data_url)
    for d in dir_list:
        file_path.extend(map(lambda x: train_data_url + d + '/' + x, os.listdir(train_data_url + d)))
    return file_path


def decode_file2utf8(file_path):
    """将文件从GB2312编码解码为utf8文件"""
    decode_error = False
    file_data = []
    with open(file_path, 'r') as f:
        for l in f.readlines():
            try:
                tmp = l.decode('gbk').encode('utf8')
            except Exception as e:
                decode_error = True
                tmp = ''
            file_data.append(tmp)
    if decode_error:
        os.remove(file_path)
    else:
        with open(file_path, 'w') as f:
            f.writelines(file_data)


if __name__ == '__main__':
    for p in get_all_file_by_path():
        decode_file2utf8(p)
