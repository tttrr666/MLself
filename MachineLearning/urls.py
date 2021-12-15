from django.contrib import admin
from django.urls import path,re_path

from MachineLearning import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index),
    path('userindex',views.user_get),
    path('success',views.success),
    # path('QAsystem',views.question_answer),
    path('chat',views.chatpage),
    path('success',views.success),
    path('question',views.question),
    path('answer',views.return_answer),
]