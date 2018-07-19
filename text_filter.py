#!/usr/bin/env python
# encoding:utf-8


"""
文本过滤器
基于DFA与字典树实现的高效文本过滤器

>>>t = TextFilter()     # 初始化                       # 贪婪模式,匹配所有敏感词
>>>t.is_contain('气死我了,卧槽. 免费提供无抵押贷款')       # 监测是否有敏感词,返回(敏感词在字符串的起始位置,敏感词,敏感词类型)构成的列表
[(5, u'\u5367\u69fd', 'dirty'), (13, u'\u65e0\u62b5\u62bc\u8d37\u6b3e', 'ad')]
>>>t.filter('习近平修宪')                                # 敏感词过滤 str
***修宪
>>>t.filter(u'卧槽,我真是草泥马')                         # 敏感词过滤 unicode
**,我真是***
>>>t.filter(u'法论功大发好,真善忍好',replace_char=u'-')    # 敏感词过滤,指定替换字符
---大发好,真善忍好
>>>t.filter('高效低价英雄联盟代练')                        # 测试添加敏感词功能
高效低价英雄联盟代练
>>>t.add_word(u'英雄联盟代练')
>>>t.filter('高效低价英雄联盟代练')
高效低价******

author    :   @h-j-13
time      :   2018-7-19
"""

from sensitive_word import SensitiveWords


class Node(object):
    """字典树节点"""

    def __init__(self):
        self.children = None  # dict格式 {u'char1':node1, u'char2':node2...}
        self.sensitive_word = None
        self.sensitive_word_type = None


class TextFilter(object):
    """文本过滤"""

    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(TextFilter, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.root = Node()
        self.sensitive_word = SensitiveWords().sensitive_word_dict
        for word_type in self.sensitive_word.keys():
            for word in self.sensitive_word[word_type]:
                self.add_word(word, word_type)

    def add_word(self, word, word_type=u'common'):
        """向字典树里添加敏感词汇及敏感词类型"""
        # 处理编码
        if type(word) == str:
            word = word.decode('utf-8')
        # 向tire树添加节点
        node = self.root
        for i in range(len(word)):
            if not node.children:  # 该节点是叶节点
                node.children = {word[i]: Node()}
            elif word[i] not in node.children:  # note : 监测dict中是否有某个key, 用 k in d 比用 k in d.keys() 快三倍
                node.children[word[i]] = Node()
            node = node.children[word[i]]
        node.sensitive_word = word  # 在最后一个节点上记录整个词
        node.sensitive_word_type = word_type

    def is_contain(self, message):
        """监测文本是否含有字典树的敏感词
        返回一个列表,每一个元祖都是敏感词(出现在字符串文中的位置,敏感词,类型)"""
        # 处理编码
        if type(message) == str:
            message = message.decode('utf-8')
        # 初始化结果变量
        result = []
        i, j, message_length = 0, 0, len(message)
        # tire树 查找
        while i < message_length:
            j = i
            p = self.root
            while j < message_length and p.children is not None and message[j] in p.children:  # 匹配最长的词
                p = p.children[message[j]]
                j = j + 1
            if p.sensitive_word:  # 查找时最后落到了敏感词叶节点上
                result.append((j - len(p.sensitive_word),
                               p.sensitive_word,
                               p.sensitive_word_type))
                i += len(p.sensitive_word)  # 直接跳跃到敏感词下一个字符进行继续匹配
            else:
                i += 1
        return result

    def filter(self, message, replace_char=u'*'):
        """过滤文本,将其中的敏感词替换为过滤字符(默认为*)"""
        # 处理编码
        if type(message) == str:
            message = message.decode('utf-8')
        res = self.is_contain(message)
        for (i, word, _) in res:
            message = message[:i] + u"".join([replace_char for _ in xrange(len(word))]) + message[i + len(word):]
        return message


