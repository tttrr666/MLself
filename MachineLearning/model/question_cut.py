#encoding=utf-8
import math
import pickle
from lib2to3.pgen2.tokenize import Double
from time import sleep

import jieba
import numpy
import numpy as np
from MachineLearning.model.data_into_sql import put_data
from MachineLearning.model.test import load_variavle

class cutquestion:

    filecontent=""
    stopconent=[]
    userdict=[]

    # 如果是TXT文本，则就要求输入路径
    def __init__(self,content):
        self.filecontent=content

    # 文本内容的添加
    def content_get(self,content):
        self.filecontent=self.filecontent+str(content)
        print("this is filecontent",self.filecontent)

    # 停用词的获取
    def stopcontent(self,stopwords):
        self.stopconent=stopwords
    # 分词
    # def content_cut(self):
    #     seg_list=jieba.cut(self.filecontent,cut_all=True)
    #     print("Result words:","/".join(seg_list))
    #     return seg_list

    # 单个语句进行分词
    def content_cut(self,sentence):
        print(sentence)
        seglist=list(jieba.cut(str(sentence)))
        print("Result words:", "/".join(seglist))
        return seglist

    # 返回分词的结果
    def get_word(self):
        # 从数据库中进行拿文本【question】的文本
        # 目的是进行分词操作
        sqllink=put_data("null")
        sql = "select question_content from questions;"
        sqllink.sql_input(sql)
        data = sqllink.get_data()
        # 问题是一次只能够拿出60000条数据
        sqllink.sql_over()
        sqllink.sql_end()
        # stopwords为停用词list
        stopwords = [line.strip() for line in
                     open('../data/stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
        count=0
        result_list=[]
        for word in data:
            # 设置utf8的读取模式
            # 这一步的目的是获取所有的文本字符
            seg_list=self.content_cut(word)
            for word in seg_list:
                print("seg_list word:",word,type(word))
                if word not in stopwords:
                    result_list.append(word)
                    print(count,word)
                else:
                    print("停用词：",word)
            count=count+1
            if count==100:
                break
        return result_list

    # 词频统计
    def tf(self):
        counts={}
        countsidf={}
        sqllink = put_data("null")
        sql = "select question_content from questions;"
        sqllink.sql_input(sql)
        data = sqllink.get_data()
        sqllink.sql_over()
        sqllink.sql_end()
        stopwords = [line.strip() for line in
                     open('../data/stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
        count = 0
        for sentense in data:
            print("这是第{}条语句：内容为{}".format(count,sentense))
            count=count+1
            words=jieba.lcut(str(sentense))
            temp = []
            for word in words:
                if word not in stopwords:
                    if len(word)==1:
                        continue
                    else:
                        counts[word]=counts.get(word,0)+1
                        if word not in temp:
                            temp.append(word)
                # else:
                    # print("停用词：", word)
            for i in temp:
                countsidf[i] = countsidf.get(i, 0) + 1
            # 测试功能是否正常的用处，实际情况中可以去除
            # count=count+1
            # if count==10:
            #     break
        # items=list(counts.items())
        # items.sort(key=lambda x:x[1],reverse=True)
        # # for item in items:
        # #     word, count = item
        # #     print("词语:【{}】,出现次数:{}".format(word, count))
        # idftemp=list(countsidf.items())
        # idftemp.sort(key=lambda x:x[1],reverse=True)
        # # for idf in idftemp:
        # #     word,count=idf
        # #     print("词语:【{}】,出现的文本:{}".format(word, count))
        # return items,idftemp
        counts = sorted(counts.items(), key=lambda d: d[1], reverse=True)
        countsidf = sorted(countsidf.items(), key=lambda d: d[1], reverse=True)
        self.save_variable(counts,"tfdict.txt")
        self.save_variable(countsidf,"idfdict.txt")

    # 存储变量进入文本
    def save_variable(self,v, filename):
        f = open(filename, 'wb')
        pickle.dump(v, f)
        f.close()
        return filename

    # 取出存储的变量
    def load_variavle(self,filename):
        f = open(filename, 'rb')
        r = pickle.load(f)
        f.close()
        return r

    # 获取总词频数目与文本的数目[对列表中出现的所有数据进行统计与计数]
    def count_result(self,count):
        all_count_number=0
        for i in count.keys():
            # print(word,num)
            all_count_number=all_count_number+count[i]
        return all_count_number

    # 把list类型转化成字典类型
    def list_to_dict(self,list):
        dict={}
        for i in range(len(list)):
            dict[list[i][0]]=list[i][1]
        return dict

        # 通过tf-idf算法进行计算每一个词向量的权重
        # 当我们的数据存储的数据结构是dictionary类型时，
        # 要对dictionary数据类型进行获取

    def reslut_tdidf(self, tf, idf):
        word_dictionary = {}
        # 这里使用的是字典类型
        tf = load_variavle(tf)
        idf = load_variavle(idf)
        # word_dictory=tf
        # 这个地方获取我们所需要的词频总数与总文档的数目
        tf=self.list_to_dict(tf)
        idf=self.list_to_dict(idf)
        all_tf = self.count_result(tf)
        # 总文档数目可以从数据库中获取
        all_idf = 60000
        print("总词数目：",all_tf)
        # 这个地方使用count是为了测试，因为数据量很大
        # 如果对循环进行中断的话那么所花费的时间就会比较的长
        # 不利于代码编写人员进行测试
        # count = 0
        for key in tf.keys():
            # tf=该词语出现的次数/该文本的总词语数目
            # idf=ln(语料库中的文件总数/包含词语的文件数目（即的文件数目）)
            # tf-idf=tf*idf
            # print(word, num)
            word_dictionary[key] = (tf[key] / all_tf) * (math.log((all_idf / (idf[key] + 1)), math.e))
            # if count == 10:
            #     break
            # else:
            #     count = count + 1
        return word_dictionary
a=cutquestion("")
# td,idf=a.tf()
# fileaname=save_variable(td,"td.txt")
# fileaname1=save_variable(idf,"idf.txt")
# testa=load_variavle("td.txt")
# testb=load_variavle("idf.txt")
# print(testa,testb)
result=a.reslut_tdidf("tfdict.txt","idfdict.txt")
a.save_variable(result,"tfidf.txt")
# print("result:",result)
for i in result.keys():
    print("词语:【{}】,tf-idf:{}".format(i, result[i]))