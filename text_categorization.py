# -*-coding:utf-8-*- 

import jieba.posseg as pesg
import codecs
import sys
from gensim import corpora,models,similarities
import os
allFileNum = 0

reload(sys)
sys.setdefaultencoding('utf8')

class XiangSi():
    def __init__(self):
        #构建停用词表
        self.stop_words='D:/' + u'py程序' + '/stopwords.txt'
        self.stopwords=codecs.open(self.stop_words,'r',encoding='utf-8').readlines()
        self.stopwords=[w.strip()for w in self.stopwords]
        self.stop_flag=['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
#对文章进行分词、去停用词
    def tokenzation(self,filename):
        result=[]
        with open(filename,'r') as f:
            text=f.read()
            words=pesg.cut(text)#
        for word,flag in words:
            if flag not in self.stop_flag and word not in self.stopwords:
                result.append(word)
        return result
    def wenzhang(self,files,example):
        filenames=files
        corpus=[]
        for each in filenames:
            corpus.append(self.tokenzation(each))
        #建立词袋模型
        dictionary=corpora.Dictionary(corpus)
        doc_vectors=[dictionary.doc2bow(text) for text in corpus]
        #建立TF-IDF模型
        tfidf=models.TfidfModel(doc_vectors)
        tfidf_vectors=tfidf[doc_vectors]
		#指定主题数
        lsi=models.LsiModel(tfidf_vectors,id2word=dictionary,num_topics=5)
        lsi = models.LsiModel(tfidf_vectors, id2word=dictionary)
        lsi_vector=lsi[tfidf_vectors]
		
        #构建训练样本
        query=self.tokenzation('D:/' +'ZNdaolun/Sun/' + example)
		
        query_bow=dictionary.doc2bow(query)
        query_lsi=lsi[query_bow]
        index=similarities.MatrixSimilarity(lsi_vector)
        sims=index[query_lsi]
        #print list(enumerate(sims))
        return list(enumerate(sims))
    def analyse_nr(self,filepath):
        listfiles=[]
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            child.decode('utf-8')
            listfiles.append(child)
        return listfiles
            #print child.decode('utf-8')  # .decode('gbk')是解决中文显示乱码问题
    def maopao(self,list1):
        j = 0
        for i in range(len(list1)):
            for j in range(len(list1) - i - 1):
                if (list1[j][1] < list1[j + 1][1]):
                    t = list1[j]
                    list1[j] = list1[j + 1]
                    list1[j + 1] = t
        print list1
    def token1(self,text,topic):
        result=[]
        words=pesg.cut(text)#
        for word in words:
            if word in self.stopwords:
                result.append(word)
        return result

    def printPath(self,level, path):
        global allFileNum
        # 所有文件夹，第一个字段是次目录的级别
        dirList = []
        # 所有文件
        fileList = []
        # 返回一个列表，其中包含在目录条目的名称(google翻译)
        files = os.listdir(path)
        # 先添加目录级别
        dirList.append(str(level))
        for f in files:
            if (os.path.isdir(path + '/' + f)):
                # 排除隐藏文件夹。因为隐藏文件夹过多
                if (f[0] == '.'):
                    pass
                else:
                    # 添加非隐藏文件夹
                    dirList.append(f)
            if (os.path.isfile(path + '/' + f)):
                # 添加文件
                fileList.append(f)
                # 当一个标志使用，文件夹列表第一个级别不打印
        i_dl = 0
        for dl in dirList:
            if (i_dl == 0):
                i_dl = i_dl + 1
            else:
                # 打印至控制台，不是第一个的目录
                print '-' * (int(dirList[0])), dl
                # 打印目录下的所有文件夹和文件，目录级别+1
                self.printPath((int(dirList[0]) + 1), path + '/' + dl)
        # for fl in fileList:
        #     # 打印文件
        #     print '-' * (int(dirList[0])), fl
        #     # 随便计算一下有多少个文件
        #     allFileNum = allFileNum + 1
        return fileList

    def change1(self,list1, list2, str1):
        for i in range(len(list1)):
            newnum = list1[i][1]
            newstr = str(list1[i][0]) +'-'+str(list2[i])+'-'+ str1
            list1[i] = (newstr, newnum)
        return list1
if __name__=='__main__':
    xs=XiangSi()
    listfile=xs.printPath(1, 'D:/ZNdaolun/Sun/text')
    count=1
    list6=[]
    #files=['D:/' + u'py程序' + '/answer/1.txt','D:/' + u'py程序' + '/answer/people_top10.txt','D:/' + u'py程序' + '/answer/p_location.txt']

    files=xs.analyse_nr('D:/' +'ZNdaolun' + '/Sun/text/')
    #print files
    #区分类别，根据需要更改类别文件
    list1=xs.wenzhang(files,'computer.txt')
    list1=xs.change1(list1,listfile,"computer")
    list2 = xs.wenzhang(files, 'educate.txt')
    list2=xs.change1(list2, listfile, "educate")
    list3 = xs.wenzhang(files, 'sport.txt')
    list3=xs.change1(list3, listfile, "sport")
    list4 = xs.wenzhang(files, 'war.txt')
    list4=xs.change1(list4, listfile, "war")
    list5 = xs.wenzhang(files, 'weather.txt')
    list5=xs.change1(list5, listfile, "weather")
    for i in range(len(list1)):
        if list1[i][1]<list2[i][1]:
            list6.append(list2[i])
        else:
            list6.append(list1[i])
    for i in range(len(list1)):
        if list6[i][1] < list3[i][1]:
            list6[i]=list3[i]
    for i in range(len(list1)):
        if list6[i][1] < list4[i][1]:
            list6[i] = list4[i]
    for i in range(len(list1)):
        if list6[i][1] < list5[i][1]:
            list6[i] = list5[i]
    # count+=1
    # print list1,u'高血压','\n',list2,'ios','\n',list3,'android','\n',list4,'lee','\n',list5,'zhou'
    # print xs.printPath(1, 'D:/ZNdaolun/text')
    for i in range(len(list6)):
        print list6[i][1]
        if list6[i][1]<0.3:
            list6[i]=(list6[i][0],"no")
    print list6



