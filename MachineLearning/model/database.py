# -*- coding:utf-8 -*-
from pymysql import Connection
import numpy as np

class mysqluse:
    # dataplace
    mysqlhost="localhost"
    mysqluser="root"
    mysqlpasswd="zsh980521"
    mysqlport=3306
    mysqldatabase="zhushdatabase"
    sqlwords="show tables;"
    conn=Connection(host=mysqlhost,user=mysqluser,passwd=mysqlpasswd,port=mysqlport,database=mysqldatabase)

    def __init__(self):
        print("connecting mysql........")

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

    def addsql(self,sql):
        if sql:
            self.sqlwords +=sql
        else:
            print("请输入SQL语句，不要输入空字符串。")

    def replacesql(self,sql):
        if sql:
            self.sqlwords = sql
        else:
            print("请输入SQL语句，不要输入空字符串。")

    def insertsql(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(self.sqlwords)
            self.conn.commit()
        except:
            print("输入的SQL语句格式有错：{}".format(self.sqlwords))
        finally:
            cursor.close()

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

    def conn_close(self):
        self.conn.close()