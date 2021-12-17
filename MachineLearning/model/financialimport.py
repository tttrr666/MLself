from MachineLearning.model.database import mysqluse
import pandas as pd

def data_import():
    a=mysqluse()
    df=pd.read_excel('../data/金融问答集.xlsx')
    data=df.values
    for i in data:
        sql="insert into financial(idcontent,question,answer) values("+str(i[0])+",'"+str(i[1])+"','"+str(i[2])+"');"
        a.replacesql(sql)
        a.insertsql()
        print(sql)
data_import()