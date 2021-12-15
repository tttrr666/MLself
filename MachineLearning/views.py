from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
# 项目进入默认的首页面
<<<<<<< HEAD
from MachineLearning.model.question_answer import answersystem


=======
>>>>>>> c8d7091ee88043c59ce4b6e14d39091267700cdd
def index(request):
    return render(request,"index.html")
def success(request):
    return render(request,"SUCCESS.html")
def user_get(request):
    content=request.POST.get("content")
    print(content)
<<<<<<< HEAD
    return render(request,"index.html",{"next_url":success})
# 智能问答系统
# qasystem=answersystem()
# def question_answer(request):
#     uesrquestion=request.POST.get("userquestion")
#     print(uesrquestion)
#     return render(request,"",{"answer":"回答的答案！"})
def chatpage(request):
    return render(request,"chat.html")
=======
    return render(request,"index.html",{"next_url":success})
>>>>>>> c8d7091ee88043c59ce4b6e14d39091267700cdd
