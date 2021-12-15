import pandas as pd
class datadeal:
    filepath=""
    file_content=""
    def __init__(self,filepath):
        self.filepath=filepath
    def file_exist_txt(self):
        try:
            rows=open(self.filepath).read()
        except:
            rows=""
            print("The file doesnot exist!")
        finally:
            self.file_content=rows
            print("check over")

    def file_exist_csv(self):
        try:
            rows=pd.read_csv(self.filepath)
        except:
            rows=""
            print("The file doesnot exist!")
        finally:
            self.file_content=rows
            print(self.filepath)
            print("check over")

    def file_to_string(self):
        if self.file_content.size!=0:
            array=self.file_content.values
            return array
        else:
            return "error"
# 测试函数部分
# a=datadeal("../data/answers.csv")
# a.file_exist_csv()
# # a.file_to_string()
# print(a.file_to_string())