import csv
f=r"../data/financezhidao_filter.csv"
file=csv.reader(open(f,encoding="utf-8"))
count=1
f2=open('../data/q_a.csv','w',encoding='utf-8',newline="")
csv_writer=csv.writer(f2)
csv_writer.writerow(["id","question","answer"])
for i in file:
   id=count
   question=i[0]
   answer=i[2]
   if len(question)!=0 and len(answer)!=0:
      print(str(count),question,answer)
      csv_writer.writerow([str(count),question,answer])
   count+=1
f2.close()