import json
from time import sleep

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
# 项目进入默认的首页面
from MachineLearning.FAQsystem.system import system
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
        return JsonResponse({"url": "http://localhost:8000/chat"})
    else:
        return render(request,"index.html")
def chatpage(request):
    return render(request,"chat.html")
# a=answersystem()
a=system()
a.sentense_get()
a.limit_low_words(1)
a.word_tfidf()
def question(request):
    question=request.POST.get("question")
    print(question)
    answer=a.userquestion(question)
    return JsonResponse({"answer": answer})
# def return_answer(request):
#     global answer
#     while len(answer)!=0:
#         if len(answer)!=0:
#             return JsonResponse({"answer":answer})
#         else:
#             return JsonResponse({"status":"error","answer":"null"})