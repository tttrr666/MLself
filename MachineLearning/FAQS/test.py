from MachineLearning.FAQS.common.connecting import connecting_sql
from MachineLearning.FAQS.firstcallback.answ_1 import first_answer

a=first_answer()
sqlconnect = connecting_sql()
a.modelpre("financial")
for i in range(10):
    question=input("question:")
    answer=a.question_get(question)
    for i in answer:
        print(i)
    sql="select question,answer from financial where idcontent="+answer[0][0]
    sqlconnect.replacesql(sql)
    print(sqlconnect.outsql())
    print("pause...")