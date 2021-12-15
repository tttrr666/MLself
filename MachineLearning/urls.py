from django.contrib import admin
from django.urls import path,re_path

from MachineLearning import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index),
    path('userindex',views.user_get,name='userindex'),
<<<<<<< HEAD
    path('success',views.success),
    # path('QAsystem',views.question_answer),
    path('chat',views.chatpage),
=======
    path('success',views.success)
>>>>>>> c8d7091ee88043c59ce4b6e14d39091267700cdd
]