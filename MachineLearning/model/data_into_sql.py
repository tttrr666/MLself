from pymysql import Connection
import numpy as np
from MachineLearning.model.jsontoexcel import datadeal
class put_data:
    # data
    filepath=""
    sql=""
    # 本地数据库
    # conn = Connection(host="116.62.193.114",
    #     user="zhushdatabase", passwd="mynx8tFjZ8yExm5R",
    #     port=3306, database="zhushdatabase")
    # 外网数据库
    conn = Connection(host="localhost",
                      user="root",
                      passwd="zsh980521", port=3306,
                      database="zhushdatabase")
    cursor = conn.cursor()
    # 初始化函数
    def __init__(self,filepath):
        self.filepath=filepath
        print("We had got filepath")
    # 数据库连接
    def connect_mysql(self):
        try:
            if(len(self.sql)==0):
                self.sql="show tables;"
                print("没有sql语句，请输入SQL语句")
            self.cursor.execute(self.sql)
            print(self.cursor.fetchall())
            self.sql=""
        except:
            print("数据库中的相关配置出错或是mysql数据库不存在")
    # SQL语句不断叠加
    def sql_input(self,sql):
        self.sql=self.sql+str(sql)
    # SQL语句提交
    def sql_over(self):
        self.conn.commit()
    # 游标关闭
    def sql_end(self):
        self.cursor.close()
    def get_data(self):
        try:
            if(len(self.sql)==0):
                self.sql="show tables;"
                print("没有sql语句，请输入SQL语句")
            self.cursor.execute(self.sql)
            data=np.array(self.cursor.fetchall())
            # data=self.cursor.fetchall()
            return data
        except:
            print("数据库中的相关配置出错或是mysql数据库不存在")
# a=put_data("null")
# # a.connect_mysql()
# b=datadeal("../data/answers.csv")
# # b=datadeal("../data/questions.csv")
# # # b=datadeal("../data/answers.csv")
# b.file_exist_csv()
# array=b.file_to_string()
# count=0
# for i in array:
#     # i[1]=str(i[1]).replace("'",",")
#     sql=r'insert into question_answer(answer_id,question_id) values ( '+str(i[0])+r",'"+str(i[1])+r"');"
#     a.sql_input(sql)
#     print(sql)
#     a.connect_mysql()
#     a.sql_over()
#     count=count+1
#     if count==10:
#         count=0
#         print(str(count)+"____________________________________________")
#         a.connect_mysql()
# a.sql_end()
# print("result:"+a.sql)
