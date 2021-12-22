from pymysql import Connection


class connectsql:
    mysqlhost = "localhost"
    mysqluser = "root"
    mysqlpasswd = "zsh980521"
    mysqlport = 3306
    mysqldatabase = "zhushdatabase"
    sqlwords = "show tables;"
    conn = Connection(host=mysqlhost,
                      user=mysqluser,
                      passwd=mysqlpasswd,
                      port=mysqlport,
                      database=mysqldatabase)
    def __init__(self):
        print("connecting mysql ...")
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