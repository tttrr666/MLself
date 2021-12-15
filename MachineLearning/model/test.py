from MachineLearning.model.question_answer import answersystem

a=answersystem()
# 问题集处理
# a.cut_questions()
# 统计图展示
# a.showplot()
# 处理低频词汇
# a.wordtfidf(1000)
# # 模型保存
# a.save_model()
# a.question_transport()
# a.matrix()
# a.save_model()
# print(len(a.transported_question["治疗"]))
# print(a.transported_question.keys())
print(a.worddict)
for i in range(10):
    question=input("输入问题：")
    a.question_answer(question)
    input("pause continue...")
# 医生,您好.我于今年3月早产(孕34周破水急产,造成宝宝重度缺氧缺血性脑病夭折),是顺产.现在时隔三个月发现又怀孕了,请问我能顺利要这个宝宝吗?这次还会不会再发生早产呢?我要注意什么呢?