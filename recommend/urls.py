from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static 
from . import views
from django.views.static import serve

from django import urls
from django.conf.urls import url

urlpatterns = [
    path('getm/', view=views.get_movies),  #推荐页面
    path('login/', view=views.login),  #登录
    path('getmsim/', view=views.get_movies_sim), #“和你类似的用户还喜欢看”的电影信息
    path('minfo/', view=views.getm_info), #单独电影页面的信息

    path('images/', view=views.read_img), #暂时没用
]


