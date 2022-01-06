# 第一次粗召回
# 返回前20的答案
import math

from MachineLearning.FAQS.common.startjieba import startjieba
from MachineLearning.FAQS.funcmodels.tfidf import tfidf


class first_answer:
    def __init__(self):
        print("第一次粗召")
    def modelpre(self,sqltable):
        self.questionsystem = tfidf()
        self.questionsystem.sentense_get(sqltable)
        self.questionsystem.word_tfidf()
        self.questionsystem.sortmartix()
        # 加载tfidf，建立倒排索引
    def question_get(self,question):
        # 问题分词
        seglist=self.questionsystem.cut_stop_words(startjieba().all_cut(question))
        seg_dict={}
        for i in seglist:
            if i in seg_dict:
                seg_dict[i]+=1
            else:
                seg_dict[i]=1
        # 生成问题向量_____________________________________________
        question_vector=[]
        # 问题向量
        question_vector_row=[]
        # 问题向量对应的列
        systemdata_vector={}
        # 数据集向量
        vector_row=[]
        # 文档编号
        answer_list=[]
        # 文本档案编号
        for i in self.questionsystem.system_ES.keys():
            if i in seglist:
                question_vector_row.append(i)
                question_vector.append(seg_dict[i]/len(seglist)*math.log((self.questionsystem.alldoc / self.questionsystem.system_ES[i][0] + 2), math.e))
                temp=self.questionsystem.system_ES[i][2].keys()
                answer_list.append(self.questionsystem.system_ES[i][2])
                for j in temp:
                    if j not in vector_row:
                        vector_row.append(j)
        for i in vector_row:
            temp=[]
            for j in range(len(question_vector_row)):
                if i in answer_list[j].keys():
                    temp.append(answer_list[j][i][1])
                else:
                    temp.append(0)
            systemdata_vector[i]=temp
        systemdata=[]
        for i in systemdata_vector:
            systemdata.append([i,self.cosVector(systemdata_vector[i],question_vector)])
        systemdata=self.sortmartix(systemdata)
        return systemdata


    def cosVector(self, x, y):
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
        cosresult = result1 / ((result2 * result3) ** 0.5)
        return cosresult
    def sortmartix(self,estable):
        resultestable=sorted(estable,key=lambda docidf:docidf[1],reverse=True)
        return resultestable