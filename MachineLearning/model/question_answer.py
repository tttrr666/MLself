#encoding=utf-8
import math
import pickle
import jieba
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

from MachineLearning.model.database import mysqluse


class answersystem:
    mysqldatabase=mysqluse()
    # 词频v
    wordtf={}
    # 文本频率
    wordidf={}
    # 词袋
    worddict=[]
    # tfidf
    alltfidf={}
    # 向量化文本【倒排结构】
    transported_question={}
    # 向量化文本【非倒排结构】
    question_matrix=[]
    operating="saved"
    # 是否需要对数据进行保存

    def __init__(self):
        print("问答系统启动")
        if self.operating=="saved":
            self.wordtf=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_wordtf.txt")
            self.wordidf=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_wordidf.txt")
            self.worddict=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_worddict.txt")
            self.alltfidf=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_tfidf.txt")
            self.transported_question=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_question.txt")
            self.question_matrix=self.load_variavle("F:\pythonproject\MLself\MachineLearning\model\system_question_martix.txt")
            print("模型载入成功！")

# 输入SQL语句返回问题列表
    def get_questions(self,sql):
        self.mysqldatabase.replacesql(sql)
        questions=self.mysqldatabase.outsqls()
        return questions
# 模型数据的保存
    def save_model(self):
        if self.operating=="save":
            self.save_variable(self.wordtf,"F:\pythonproject\MLself\MachineLearning\model\system_wordtf.txt")
            self.save_variable(self.wordidf,"F:\pythonproject\MLself\MachineLearning\model\system_wordidf.txt")
            self.save_variable(self.worddict,"F:\pythonproject\MLself\MachineLearning\model\system_worddict.txt")
            self.save_variable(self.alltfidf,"F:\pythonproject\MLself\MachineLearning\model\system_tfidf.txt")
            self.save_variable(self.transported_question,"F:\pythonproject\MLself\MachineLearning\model\system_question.txt")
            self.save_variable(self.question_matrix,"F:\pythonproject\MLself\MachineLearning\model\system_question_martix.txt")
            print("保存系统数据成功！")
        else:
            print("保存数据失败")
# 输入查询返回结果
    def get_answer(self,sql):
        self.mysqldatabase.replacesql(sql)
        answer=self.mysqldatabase.outsql()
        return answer
# 对单个的文档进行分词
    def cut_question(self,userquestion):
        seg_list=list(jieba.lcut(userquestion))
        print("问题进行分词后的结果为:", "/".join(seg_list))
        return seg_list
# 将分词好的文档进行tfidf词频与文档频率进行统计
    def counttf(self,seg_list):
        # stopwords = [line.strip() for line in
        #              open('F:\pythonproject\MLself\MachineLearning\data\stopwords\cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords=[]
        temp=[]
        for word in seg_list:
            if word not in stopwords:
                if word not in self.wordtf.keys():
                    self.wordtf[word]=1
                else:
                    self.wordtf[word] =self.wordtf.get(word)+1
                if word not in temp:
                    temp.append(word)
        for sentense in temp:
            if sentense not in self.wordidf:
                self.wordidf[sentense] = 1
            else:
                self.wordidf[sentense] += 1
# 对tfidf等数据进行排序【字典】
    def sortwordtfandidf(self):
        wordidftemp={}
        self.wordtf=dict(sorted(self.wordtf.items(),key = lambda x:x[1],reverse = True))
        for word in self.wordtf:
            wordidftemp[word]=self.wordidf[word]
        self.wordidf=wordidftemp
# 问题集的处理
    def cut_questions(self):
        # sql="select count(question_id) from questions;"
        sql="select count(idcontent) from financial;"
        self.mysqldatabase.replacesql(sql)
        questionscount=self.mysqldatabase.outsql()[0][0]
        # time=questionscount//10000
        time = 1
        for i in range(time):
            # sql=r"select question_content from questions limit "+str(i*10000+1)+","+"10000;"
            sql = r"select question from financial;"
            print("分词部分：执行第{}次查询的语句为：".format(i+1),sql)
            questiondata=self.get_questions(sql)
            for sentence in questiondata:
                print(sentence)
                seg_list = list(jieba.lcut(str(sentence)))
                self.counttf(seg_list)
        self.sortwordtfandidf()
# 对变量进行存储
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

# 对tf词频进行统计
    def showplot(self):
        self.sortwordtfandidf()
        y=[]
        for i in self.wordtf:
            y.append(self.wordtf[i])
        plt.plot(sorted(y,reverse=True)[50:])
        plt.show()
# 统计总词频
    def count_reslut(self):
        allcount=0
        for i in self.wordtf:
            allcount+=self.wordtf[i]
        return allcount
# 低频词处理
    def wordtfidf(self,limit):
        self.sortwordtfandidf()
        worddict=[]
        alltfidf={}
        # sql = "select count(question_id) from questions;"
        sql = "select count(idcontent) from financial;"
        self.mysqldatabase.replacesql(sql)
        allidf= self.mysqldatabase.outsql()[0][0]
        alltf=self.count_reslut()
        for i in self.wordtf:
            if self.wordtf[i]>=limit:
                worddict.append(i)
                alltfidf[i]=(self.wordtf[i]/alltf)*(math.log((allidf/self.wordidf[i]+1),math.e))
                print(i,"___________",alltfidf[i],"__________")
        self.worddict=worddict
        self.alltfidf=alltfidf
# 词频计算
    def counttime(self,seg_list):
        seglist={}
        for i in seg_list:
            if i not in seglist:
                seglist[i]=1
            else:
                seglist[i]+=1
        return seglist
# 文本向量的转化
    def question_transport(self):
        for i in self.worddict:
            self.transported_question[i]=[]
        # sql = "select count(question_id) from questions;"
        sql = "select count(idcontent) from financial;"
        self.mysqldatabase.replacesql(sql)
        questionscount = self.mysqldatabase.outsql()[0][0]
        # time = questionscount // 10000
        time = 1
        t=1
        for i in range(time):
            # sql=r"select question_content from questions limit "+str(i*10000)+","+"10000;"
            sql = r"select question from financial;"
            print("词向量转化部分：执行第{}次查询的语句为：".format(i + 1), sql)
            questiondata = self.get_questions(sql)
            print(i,len(questiondata))
            for sentence in questiondata:
                print(t,"______________________________________________")
                # print(sentence)
                # print("____________________________________________________")
                seg_list = self.counttime(list(jieba.lcut(str(sentence))))
                for i in self.transported_question.keys():
                    if i not in seg_list.keys():
                        self.transported_question[i].append(0)
                    else:
                        self.transported_question[i].append(seg_list[i] * self.alltfidf[i])
                # print(self.transported_question,"/n_______________________question______________________")
                # print(t)
                t+=1
            del questiondata
        # print(self.transported_question)
# 问答入口
    def matrix(self):
        juzhen=[]
        for i in self.transported_question.keys():
            juzhen.append(self.transported_question[i])
        juzhen=list(map(list, zip(*juzhen)))
        self.question_matrix=juzhen
    def question_answer(self,question):
        questionlist={}
        questionarray=[]
        location=[]
        seg_list=self.counttime(list(jieba.lcut(question)))
        for i in self.worddict:
            if i not in seg_list:
                questionarray.append(0)
            else:
                questionarray.append(self.alltfidf[i]*seg_list[i])
                print(i)
                location.append(self.transported_question[i])
                if i not in questionlist.keys():
                    questionlist[i]=1
                else:
                    questionlist[i]+=1
        location1=np.array(location)
        temp=np.transpose(np.nonzero(location1))
        addre=[]
        for i in range(len(temp)):
            if temp[i][1] not in addre:
                addre.append(temp[i][1])
        answer=[]
        answeradd=[]
        for i in addre:
            answer.append(cosine(self.question_matrix[i],questionarray))
            answeradd.append(i)
        a=addre[answer.index(max(answer))]
        # sql="select question_id from questions limit "+str(a)+",1;"
        # self.mysqldatabase.replacesql(sql)
        # questionid=self.mysqldatabase.outsql()[0][0]
        # sql="select answer_id from question_answer where question_id="+str(questionid)+";"
        # self.mysqldatabase.replacesql(sql)
        # answerid=self.mysqldatabase.outsql()[0][0]
        # sql="select answer_content from answers where answer_id="+str(answerid)+";"
        sql = "select question from financial where idcontent=" + str(a+1) + ";"
        self.mysqldatabase.replacesql(sql)
        print(self.mysqldatabase.outsql()[0][0])
        sql = "select answer from financial where idcontent=" + str(a + 1) + ";"
        self.mysqldatabase.replacesql(sql)
        print(self.mysqldatabase.outsql()[0][0])
        return str(self.mysqldatabase.outsql()[0][0])