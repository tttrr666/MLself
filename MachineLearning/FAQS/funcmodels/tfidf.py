# 用于计算tfidf并产生ES表，生成文档向量，词袋等功能
import math

from MachineLearning.FAQS.common.connecting import connecting_sql
from MachineLearning.FAQS.common.startjieba import startjieba


class tfidf:
    # es倒排索引表
    system_ES = {}
    # 连接数据库配置
    sqlconnect = connecting_sql()
    cut_sentense = startjieba()
    alldoc = 0
    all_file_tf={}
    # 启动函数
    def __init__(self):
        print("数据库中文本处理中......")

    # 数据库配置信息进行修改
    def change_sql(self,hostname,user,passwd,port,database):
        try:
            self.sqlconnect.replaceconn(hostname, user, passwd, port, database)
            print("修改数据库配置信息成功")
        except:
            print("数据库配置信息修改失败")

    # 从数据库中进行数据的拿取
    def sentense_get(self,tablename):
        # 拿取数据库某个表中的数据总数
        sql="select count(*) from "+tablename+";"
        self.sqlconnect.replacesql(sql)
        count=self.sqlconnect.outsql()[0][0]
        if count <= 10000:
            sql = "select idcontent,question,answer,label from "+tablename+";"
            self.sqlconnect.replacesql(sql)
            sqldata = self.sqlconnect.outsqls()
            for i in sqldata:
                self.create_es(i)
        else:
            time=count//10000
            for i in range(time+1):
                sql="select idcontent,question,answer,label from "\
                    +tablename+" limit "+str(i*10000)\
                    +",10000;"
                self.sqlconnect.replacesql(sql)
                sqldata=self.sqlconnect.outsqls()
                for i in sqldata:
                    self.create_es(i)
    # 从数据库中指定的表拿数据进行构建es表
    def create_es(self, single_data):
        docfile = single_data[0]
        # 文档ID
        question = single_data[1]
        # 问题
        answer = single_data[2]
        # 答案
        label=single_data[3]
        # 用户情感标签
        question_list = self.cut_sentense.all_cut(question)
        # 分词
        question_list = self.cut_stop_words(question_list)
        # 去除停用词
        self.all_file_tf[docfile]=len(question_list)
        # 该文档的总词数
        count = 1
        # 文本位置信息记录，起始位置：1
        for i in question_list:
            if i not in self.system_ES.keys():
                # 判断该词是否在es表中，不在则就进行添加
                location_table={}
                # 文档位置信息
                location_table[docfile]=[1,0,[count]]
                # 第一位：该文档中的词频，第二位：该文档中该词的tfidf值，第三位：该词在该文档中的位置，键为文档的编号
                # 所有的es表格建立后才会进行第二位tfidf值
                self.system_ES[i] = [1, 1,location_table]
                # 键值：词语，第一位：文档频率，第二位：该词在整个数据集中出现的次数，第三位：位置信息
                self.alldoc+=1
                # 总文档频率记录
            else:
                # 如果这个词语在es表格中
                word_idf=self.system_ES[i][0]
                # 拿到文档频率
                word_all_tf=self.system_ES[i][1]
                # 拿到该词的总词频数
                estable=self.system_ES[i][2]
                # 拿到位置信息
                # 如果这个文档第一次出现
                if docfile not in estable.keys():
                    estable[docfile]=[1,0,[count]]
                    # 记录位置信息
                    word_idf+=1
                    # 文档频率增加
                    word_all_tf+=1
                    # 该词的总词频增加
                    self.alldoc += 1
                    # 总文档频率记录
                else:
                    # 该文档并非第一次出现
                    word_file_tf=estable[docfile][0]+1
                    # 该词在这个文档中出现的频率
                    word_file_location=estable[docfile][2]
                    word_file_location.append(count)
                    # 该词在这个文档中的位置信息与添加
                    word_all_tf += 1
                    # 该词的总词频增加
                    self.alldoc += 1
                    # 总文档频率记录
                    estable[docfile] = [word_file_tf, 0, word_file_location]
                self.system_ES[i]=[word_idf,word_all_tf,estable]
            # 一个词语处理完毕，位置信息增加1
            count+=1
    # 低频词语处理
    def limit_low_words(self, limitimes):
        for i in self.system_ES.keys():
            a = self.system_ES[i][1]
            if a < limitimes:
                for j in self.system_ES[i][2].keys():
                    self.all_file_tf[j]=self.all_file_tf[j]-self.system_ES[i][2][j][0]
                self.system_ES.pop(i)
    # 计算tfidf
    def word_tfidf(self):
        for i in self.system_ES.keys():
            word_location=self.system_ES[i][2]
            for j in word_location.keys():
                file_tf=word_location[j][0]
                file_location=word_location[j][2]
                file_tfidf=(file_tf / self.all_file_tf[j]) * \
                                   (math.log((self.alldoc / self.system_ES[i][0] + 1), math.e))
                word_location[j]=[file_tf,file_tfidf,file_location]
            self.system_ES[i]=[self.system_ES[i][0],self.system_ES[i][1],word_location]
    # 停用词
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