import math
import pickle
import numpy as np

from MachineLearning.FAQsystem.startjieba import startjieba
from MachineLearning.model.database import mysqluse


class system:
    system_ES={}
    sqlconnect=mysqluse()
    operatestatus="save"
    # save/update/saved
    cut_sentense=startjieba()
    system_tfidf={}
    allword=0
    alldoc=0

    def __init__(self):
        print("start FAQ system")
        if self.operatestatus=="saved" or self.operatestatus=="update":
            self.system_ES=self.load_variavle("F:\pythonproject\MLself\MachineLearning\data\system_ES.txt")
            print("数据载入成功！")

    def savedata(self):
        if self.operatestatus=="save":
            self.save_variable(self.system_ES,"F:\pythonproject\MLself\MachineLearning\data\system_ES.txt")
            print("数据保存成功！")
        else:
            print("系统状态错误！")

    def save_variable(self, v, filename):
        f = open(filename, 'wb')
        pickle.dump(v, f)
        f.close()
        return filename
        # 取出存储的变量
    def load_variavle(self, filename):
        f = open(filename, 'rb')
        r = pickle.load(f)
        f.close()
        return r
    # 数据库中拿句子
    def sentense_get(self):
        sql="select count(*) from financial;"
        self.sqlconnect.replacesql(sql)
        count=self.sqlconnect.outsql()[0][0]
        if count<=10000:
            sql="select idcontent,question,answer from financial;"
            self.sqlconnect.replacesql(sql)
            sqldata=self.sqlconnect.outsqls()
            for i in sqldata:
                self.create_es(i)
        else:
            time=count//10000
            for i in range(time+1):
                sql="select idcontent,question,answer from financial limit "+str(i*10000)\
                    +",10000;"
                self.sqlconnect.replacesql(sql)
                sqldata=self.sqlconnect.outsqls()
                for i in sqldata:
                    self.create_es(i)
    # 对数据库中拿到的句子进行倒排
    def create_es(self,single_data):
        docfile=single_data[0]
        question=single_data[1]
        answer=single_data[2]
        question_list=self.cut_sentense.all_cut(question)
        question_list=self.cut_stop_words(question_list)
        count=1
        temp=[]
        for i in question_list:
            if i not in temp:
                temp.append(i)
            if i not in self.system_tfidf.keys():
                self.system_tfidf[i]=0
                estable={}
                estable[docfile]=[count]
                self.system_ES[i]=[1,1,estable]
                count+=1
                self.allword+=1
            else:
                estable1=self.system_ES[i][2]
                tempcount=self.system_ES[i][1]+1
                doccount=self.system_ES[i][0]
                if docfile in estable1.keys():
                    # ******************
                    estable1[docfile].append(count)
                    self.allword+=1
                    count+=1
                else:
                    estable1[docfile]=[count]
                    self.allword+=1
                    count+=1
                self.system_ES[i]=[doccount,tempcount,estable1]
        for i in temp:
            self.system_ES[i][0]+=1
        self.alldoc+=1
    # 停用词处理
    def cut_stop_words(self,seglist):
        seg_list=[]
        # stopwords = [line.strip() for line in
        #              open('F:\pythonproject\MLself\MachineLearning\data\stopwords\cn_stopwords.txt',
        #                   'r', encoding='utf-8').readlines()]
        stopwords=[]
        for i in seglist:
            if i not in stopwords:
                seg_list.append(i)
            else:
                print("stopwords:",i)
        return seg_list
    # 低频词语处理
    def limit_low_words(self,limitimes):
        for i in self.system_ES.keys():
            a=self.system_ES[i][1]
            if a < limitimes:
                self.allword-=self.system_ES[i][1]
                self.alldoc-=self.system_ES[i][0]
                self.system_ES.pop(i)
                self.system_tfidf.pop(i)
    # 计算tfidf
    def word_tfidf(self):
        for i in self.system_ES.keys():
            self.system_tfidf[i]=(self.system_ES[i][1]/self.allword)*\
                                 (math.log((self.alldoc/self.system_ES[i][0]+1),math.e))
    # 根据问题建立数据集中的向量化
    def get_ES_result(self,word):
        word_get=[]
        for i in word:
            temp=[i,self.system_ES[i][0],self.system_ES[i][1],self.system_ES[i][2]]
            word_get.append(temp)
        word_get=self.sortmartix(word_get)
        word_dict=[]
        doc_list=[]
        sentense_martix=[]
        for i in word_get:
            word_dict.append(i[0])
            temp=i[3].keys()
            for i in temp:
                if i not in doc_list:
                    doc_list.append(i)
        for i in doc_list:
            single_doc=[]
            for j in word_dict:
                a=self.system_ES[j][2]
                if i in a.keys():
                    single_doc.append(self.system_tfidf[j]*(len(self.system_ES[j][2][i])))
                else:
                    single_doc.append(0)
            sentense_martix.append(single_doc)
        return doc_list,sentense_martix


    def sortmartix(self,estable):
        resultestable=sorted(estable,key=lambda docidf:docidf[1],reverse=True)
        return resultestable

    # 问题向量化
    def userquestion(self,question):
        result=self.cut_sentense.questioncut(question)
        question_word=[]
        question_tfidf=[]
        for i in result.keys():
            if i in self.system_tfidf.keys():
                question_word.append(i)
                question_tfidf.append(self.system_tfidf[i] * result[i])
        doc_list,doc_martix=self.get_ES_result(question_word)
        doc_rank=[]
        for i in doc_martix:
            doc_rank.append(self.cosVector(i,question_tfidf))
        question_id=doc_list[doc_rank.index(max(doc_rank))]
        sql="select answer from financial where idcontent="+str(question_id)+";"
        self.sqlconnect.replacesql(sql)
        answer =self.sqlconnect.outsql()[0][0]
        print(answer)
        return answer

    def cosVector(self,x, y):
        if (len(x) != len(y)):
            print('error input,x and y is not in the same space')
            return;
        result1 = 0.0;
        result2 = 0.0;
        result3 = 0.0;
        for i in range(len(x)):
            result1 += x[i] * y[i]  # sum(X*Y)
            result2 += x[i] ** 2  # sum(X*X)
            result3 += y[i] ** 2  # sum(Y*Y)
        # print(result1)
        # print(result2)
        # print(result3)
        cosresult= result1 / ((result2 * result3) ** 0.5)
        return cosresult

