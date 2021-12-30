# -*- coding:utf-8 -*-
# 数据库连接
# aim：
# 1：用来配置连接的数据库相关信息
# 2：用来从数据库中进行取数据等相关操作
# 3：标签分类使用
from pymysql import Connection
import numpy as np

class connecting_sql:
    mysqlhost = "localhost"
    mysqluser = "root"
    mysqlpasswd = "zsh980521"
    mysqlport = 3306
    mysqldatabase = "zhushdatabase"
    sqlwords = "show tables;"
    # 本地数据库配置
    # 在本地数据库失效的时候启用外网数据库
    def __init__(self):
        try:
            print("本地数据库启动。")
            self.conn = Connection(host=self.mysqlhost,
                                   user=self.mysqluser,
                                   passwd=self.mysqlpasswd,
                                   port=self.mysqlport,
                                   database=self.mysqldatabase)
        except:
            print("外网数据库启动。")
            self.conn=Connection(host="116.62.193.114",
                                 user="zhushdatabase",
                                 passwd="mynx8tFjZ8yExm5R",
                                 port=3306,
                                 database="zhushdatabase")
        finally:
            print("******连接数据库成功！******")
    # 数据库配置信息更改
    def replaceconn(self,host,user,passwd,port,database):
        try:
            self.conn=Connection(host,user,passwd,port,database)
            print("连接数据库成功！")
        except:
            print("连接数据库失败，请重新输入数据库的相关配"
                  "置信息：host:{} user:{} password:{} port:{} database:{}"
                  "".format(host,user,passwd,port,database))
        finally:
            print("修改数据库相关信息操作完成！")
    # 添加SQL语句，一次性执行
    def addsql(self,sql):
        if sql:
            self.sqlwords +=sql
        else:
            print("请输入SQL语句，不要输入空字符串。")
    # 替换SQL语句，单次执行
    def replacesql(self,sql):
        if sql:
            self.sqlwords = sql
            print(sql)
        else:
            print("请输入SQL语句，不要输入空字符串。")
    # 执行插入操作
    def insertsql(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.sqlwords)
            self.conn.commit()
        except:
            print("输入的SQL语句格式有错：{}".format(self.sqlwords))
        finally:
            cursor.close()
    # 输出查询得到的列表
    def outsqls(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.sqlwords)
            data = np.array(cursor.fetchall())
            self.conn.commit()
        except:
            print("输入的SQL语句格式错误：{}".format(self.sqlwords))
            data=False
        finally:
            cursor.close()
        return data
    # 输出查询得到的数值
    def outsql(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.sqlwords)
            data = cursor.fetchall()
            self.conn.commit()
        except:
            print("输入的SQL语句格式错误：{}".format(self.sqlwords))
            data = False
        finally:
            cursor.close()
        return data
    # 数据库关闭
    def conn_close(self):
        self.conn.close()