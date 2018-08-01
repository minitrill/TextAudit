文本审核模块
========
minitrill 文本审核模块

## 模块架构
![](https://upload-images.jianshu.io/upload_images/5617720-46bf7d07f7fa79e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

整体思路如下
![](https://upload-images.jianshu.io/upload_images/5617720-6246623e7fcb8d9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**核心思路**
1. 区分恶意与非恶意的文本,并给出恶意类别
2. 细化恶意类别,来展现文本的恶意程度
3. 对于**不同频率/不同程度/不同影响力**的言论采取不同程度不同方式的处理策略      
(这里直接从本模块抽离出来了,主要是对于用户进行性质分类来打击用户,参见用户特征模块)


## 文本处理
本子模块主要用于处理文本,发现恶意并判别细致的恶意类型

### 0. 文本预处理
主要是对输入的文本进行预处理和分词,主要功能包括

* 编码转换
* 字符过滤
* 分词(基于jieba分词)
  * 加载用户字典(*防止一些能够表征文本特征的词被拆分*) 
  * 停用词处理
* 词性判别

### 1. 基于文本分类的审核
是基于TF-IDF通过sklearn的实现的文本分类器及停用词,数据集持久化相关功能      
主要用于对进行预处理及分词过后的文本进行性质分类.

#### 使用说明
入口见```text_classifie.py```
```python
# 文本分类器初始化
t = TextClassifie()          # 初始化
t.set_classifie_model()      # 选择分类器模型
t.init_clf()                 # 分类器初始化(支持6种分类器模型,并且可以指定模型参数)
# 数据集构建
d = DataSet()                # 构建数据集
d.set_labels(["人", "物"])                        # 设置标签
d.add_data("我叫hj", 'train_data_1', data_labels='人')  # 添加数据(文本,id,标签)
d.add_data("这个是桌子", 'train_data_2', data_labels='物体')
tarin_data = d.train2tf_idf()                         # 生成tf-idf向量数据
# 数据集持久化,读取数据集
train_data.save_tf_idf_data()                         # 保存数据到文件中
train_data.read_tf_idf_data()                         # 从文件中读取数据
# 分类模型训练及比较
t.train(tarin_data)                                   # 训练模型
t.predicted(tarin_data)                               # 对数据进行文本分类(这里用训练数据代替)
t.metrics_result()
# 比对模型精度(只针对打好标签的训练集)
```

#### 实现功能
* 数据集
  - 自定义数据集标签集,自主添加数据
  - 使用停用词集过滤分词后的数据,并保持原语句顺序
  - 分词数据转化为TF-IDF空间向量数据
  - 支持基于PCA算法对矩阵进行降维
  - 支持持久化到磁盘中/从磁盘中读取已经训练好的数据集
  
* 分类器
  - 支持多种分类器模型进行文本分类(目前支持6种分类模型)
  - 支持自定义调参
  - 支持持久化模型当前状态到磁盘中
  - 测试集精度及性能对比
  
  
#### 性能测试
这里采用了 [文本分类语料库（复旦）测试语料](http://www.nlpir.org/?action-viewnews-itemid-103) 来进行文本分类测试      
共 **20种** 文章分类, **9374篇** 文档,共约120M,按照**7:3划分训练/测试集**进行文本分类测试       
基于 sklearn 和 TF-IDF 结合不同文本分类模型来进行文本分类测试      
文本分类测试(每种分类器经过简单调参,只展示最好的结果)结果如下 

| 文本分类器 | 训练时间(s) | 分类时间(s) | 精度 | 召回 | f1 |
| :------ | :------ | :------ | :------ | :------ | :------ |
| 多项式贝叶斯 | 0.2800 | 0.0710 | 0.86432 | 0.86929 | 0.85785 |
| 支持向量机SVM | 182.2480 | 54.6420 | 0.03297 | 0.18158 | 0.05581 |
| 决策树 | 13.9700 | 0.0410 | 0.84313 | 0.84033 | 0.84039 |
| 逻辑回归 | 13.3400 | 0.0520 | 0.82730 | 0.86558 | 0.84040 |
| 随机森林| 14.1020 | 0.2810 | 0.83121 | 0.81730 |0.79248 |
| kNN聚类 | 0.0210 | 3.1180 | 0.84410 | 0.86075 | 0.84292 |
| GBDT | 2871.2200 | 0.1640 | 0.90646 | 0.91125 | 0.90331 |

可见,经过简单调参之后GBDT的分类效果最好,f1可达0.91

此外,对于提供的恶意文本数据(*7类,500k文本量*),按照8:2划分测试及训练集,f1最终超过了0.96


#### 模型选择过程中的优缺点比较
1. 文本向量化模型

| 名称 | 含义 | 特点 |
| :------ | :------ | :------ | 
|TF-IDF| 词频-逆文档频率 | 适用性广 |
|word2vec| 词向量 | 同义词检索 |
|LAS| 潜在语义分析 | 适用主题文档 |
|TextRank| PageRank | 将词语看出网络节点 |

具体的比较和使用可以参考 [利用Python实现中文文本关键词抽取的三种方法](https://github.com/AimeeLee77/keyword_extraction)
最终选择了tf-idf来作为构建文本分类模型输入的方法.

2. 文本分类模型
这里主要就比对了贝叶斯和GBDT,由上测试结果可见       
多项式贝叶斯 : 原理简单,训练和分类时间短,分类效果优秀       
GBDT(梯度下降树) : 是几种分类器中效果最好的一个,      



### 2. 基于敏感词的文本审核及过滤
基于DFA通过tire树加简单优化实现了一个高效的敏感词过滤器,可发现文本中的所有敏感词及其类型     
并根据发现的敏感词类型对语句分类,基于敏感词性对语句进行恶意度判定

#### 实现功能
1. 共收录了6类,共744个敏感词数据
2. 基于数据库或者txt文件初始化分类初始化敏感词列表
3. 支持动态添加敏感词及类别,并可以将当前数据持久化到文件中
4. 判别语句中是否含有敏感词(默认贪婪,匹配所有敏感词)
5. 过滤语句,可以自定义过滤字符
6. 基于语句中的敏感词对句子进行恶意类别判定

#### 使用方法
入口及使用方法详见 `text_filter.py`
```python
t = TextFilter()     # 初始化                       # 贪婪模式,匹配所有敏感词
t.is_contain('气死我了,卧槽. 免费提供无抵押贷款')       # 监测是否有敏感词,返回(敏感词在字符串的起始位置,敏感词,敏感词类型)构成的列表
# [(5, u'\u5367\u69fd', 'dirty'), (13, u'\u65e0\u62b5\u62bc\u8d37\u6b3e', 'ad')]
t.filter('习近平修宪')                                # 敏感词过滤 str
# ***修宪
t.filter(u'卧槽,我真是草泥马')                         # 敏感词过滤 unicode
# **,我真是***
t.filter(u'法论功大发好,真善忍好',replace_char=u'-')    # 敏感词过滤,指定替换字符
# ---大发好,真善忍好
t.filter('高效低价英雄联盟代练')                        # 测试添加敏感词功能
# 高效低价英雄联盟代练
t.add_word(u'英雄联盟代练')
t.filter('高效低价英雄联盟代练')
# 高效低价******
t.classifie('出售幼,女私房照,小萝,莉私房,联系QQxxx')     # 文本敏感词统计(敏感词类型,出现次数) (会提前过滤符号)
# [('pron-child', 2), ('ad', 1)]
```
#### 性能测试
与python自建的in,replace性能比对

**测试集1**         
语句数量 10,000        
敏感词数量 744      

| 文本过滤器 | 运行时间(s) | 语句平均运行时间(个/ms)|
| :------ | :------ | :------ |
| 基于DFA的文本过滤器 | 0.0590 | 0.0059 |
| 朴素文本过滤器 | 0.2730 | 0.0273 |

**测试集2**        
语句数量 10000            
敏感词数量 15000 
    
| 文本过滤器 | 运行时间(s) | 语句平均运行时间(个/ms)|
| :------ | :------ | :------ |
| 基于DFA的文本过滤器 | 0.420 | 0.042 |
| 朴素文本过滤器 | 6.5060 | 0.6506 |

可以看到DFA方式的文本过滤器的速度基本是朴素写法的十倍左右              
在敏感词数据量增加的情况下性能表现也更稳定.


### 3. 针对于热度数据的人工审核接口
这里的可以视为对1,2方式的补足,主要针对以下场景. 并且审核数据可反馈1,2方式数据集

#### 作用范围
1. 传播度非常大的言论
2. 被举报多次,无法被系统识别的言论
3. 及其隐晦的政治、敏感言论

### 接口提供辅助数据
审核接口在提供需要审核的文本时也会提供一些其他数据共审核者参考

* 对于被审核文本的数据
  - 文本过滤结果
  - 文本审核结果
  - 目前文本的健康度
  
* 关联文本产生人的数据
  - 此用户近期发表言论数
  - 此用户近期健康度
  - 此用户近期被文本审核模块记录的次数
  - 此用户的影响力(粉丝数,视频数,视频点击量,喜欢数) *不展示用户个人及隐私信息*

#### 人工审核数据生成方式

1. ~~每日~ TOP1%(基于点击量) 视频标题,简介,及热评~~ (全量数据抽取过审成本太大)
2. 超过**平均传播速度** x 倍的视频所关联的评论及其他文本
3. 每日举报度(举报数 / √点击量 或 喜欢数) TOP n (*防止恶意举报?*)

## 工作流程

1. 评论文本审核
![](https://upload-images.jianshu.io/upload_images/5617720-b47e23f1db7f7668.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 资料文本(昵称,标题短文本)审核
![](https://upload-images.jianshu.io/upload_images/5617720-1cd449c8472da32f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. 举报审核
![](https://upload-images.jianshu.io/upload_images/5617720-5b4cb17783f9197d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. 反馈补充
![](https://upload-images.jianshu.io/upload_images/5617720-4d9e30ff4e7763e1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
