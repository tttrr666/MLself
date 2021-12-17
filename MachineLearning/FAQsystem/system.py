import pickle

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
        for i in question_list:
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
                if docfile in estable1.keys():
                    # ******************
                    estable1[docfile][0]+=1
                    estable1[docfile][1].append(count)
                    self.allword+=1
                    count+=1
                else:
                    estable1[docfile]=[1,[count]]
                    self.allword+=1
                    count+=1
            self.alldoc+=1
    # 停用词处理
    def cut_stop_words(self,seglist):
        seg_list=[]
        stopwords = [line.strip() for line in
                     open('F:\pythonproject\MLself\MachineLearning\data\stopwords\cn_stopwords.txt',
                          'r', encoding='utf-8').readlines()]
        for i in seglist:
            if i not in seglist:
                seg_list.append(i)
            else:
                print("stopwords:",i)
        return seg_list
    def limit_low_words(self):
        for i in self.system_ES:
            a=i[1]