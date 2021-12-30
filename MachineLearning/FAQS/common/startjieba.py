#encoding=utf-8
# jieba模块进行调用
import jieba
class startjieba:
    # 启动函数
    def __init__(self):
        print("start jieba")

        # 搜索引擎模式
    def all_cut(self,sentense):
        words=jieba.cut_for_search(sentense)
        return list(words)

    def all_lcut(self,sentense):
        words=jieba.lcut(sentense)
        return list(words)

    # 弊端：损失了位置信息
    def questioncut(self,sentense):
        word=list(jieba.cut_for_search(sentense))
        result={}
        for i in word:
            if i in result:
                result[i]+=1
            else:
                result[i]=1
        return result