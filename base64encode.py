#!/usr/bin/env python
# encoding:utf-8


"""
base64编解码处理
用于处理某些被加密的敏感词库

author    :   @h-j-13
time      :   2018-7-18
"""

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
