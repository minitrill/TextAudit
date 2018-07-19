#!/usr/bin/env python
# encoding:utf-8

import unittest
import time

from text_filter import TextFilter
from text_filter_simple import *


class Test_text_filter(unittest.TestCase):
    """不同方式实现文本过滤的性能比对"""

    def setUp(self):
        with open('C:/Users/jerryhou/Desktop/TextAuidt/test/test.txt', 'r') as f:
            test_data = f.readlines()
            self.data = []
            for item in test_data:
                self.data.append(item.strip())
            print '测试数据集大小:', len(self.data)

    def test_TextFilter(self):
        start = time.time()
        t = TextFilter()
        for s in self.data:
            t.filter(s)
        print 'TextFilter 总计用时 %.6f' % (time.time() - start)

    def test_TextfilterSimple(self):
        start = time.time()
        init_data()
        for s in self.data:
            text_filter(s)
        print 'TextFilterSimple 总计用时 %.6f' % (time.time() - start)
