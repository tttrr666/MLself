import json
from time import sleep

from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
# 项目进入默认的首页面
from MachineLearning.model.question_answer import answersystem


def index(request):
    return render(request,"index.html")
def success(request):
    return render(request,"SUCCESS.html")
def user_get(request):
    name=request.POST.get("name")
    passwd=request.POST.get("passwd")
    print(name,passwd)
    if name=="admin" and passwd=="admin":
        return render(request,"index.html",{"info":"success"})
    else:
        return render(request,"index.html")
def chatpage(request):
    return render(request,"chat.html")
a=answersystem()
answer="waiting"
def question(request):
    question=request.POST.get("question")
    print(question)
    global answer
    answer=a.question_answer(question)
    return render(request,"chat.html")
def return_answer(request):
    global answer
    while len(answer)!=0:
        return HttpResponse(answer)