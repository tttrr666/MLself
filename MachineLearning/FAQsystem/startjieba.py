#encoding=utf-8
import jieba
class startjieba:

    def __init__(self):
        print("start jieba")

        # 搜索引擎模式
    def all_cut(self,sentense):
        words=jieba.cut_for_search(sentense)
        return list(words)

    def all_lcut(self,sentense):
        words=jieba.lcut(sentense)
        return list(words)
