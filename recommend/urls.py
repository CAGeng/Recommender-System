from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static 
from . import views
from django.views.static import serve

from django import urls
from django.conf.urls import url

urlpatterns = [
    #页面信息
    path('getm/', view=views.get_movies),  #推荐页面  1
    path('getmsim/', view=views.get_movies_sim), #“和你类似的用户还喜欢看”的电影信息  1
    path('minfo/', view=views.getm_info), #单独电影页面的信息   1
    path('searchmv/', view=views.search_movie), #模糊查询电影   1
    path('gethot/', view=views.get_movie_hottest), #获取最热推荐  1
    path('simlist/', view=views.get_simlist), #获取相关电影   1

    #用户信息
    path('login/', view=views.login),  #登录  1
    path('regist/',view=views.regist), #注册  1
    path('generatecode/',view=views.generatecode), #生成验证码
    path('verifycode/',view=views.verifycode),

    #用户数据增长
    path('addrec/', view=views.add_rec),  #新增评分
    path('addbrowse/',view=views.add_browse), #新增浏览记录     1
    path('addmvsheet/',view=views.add_movie_sheet), #新增推荐电影单

    path('images/', view=views.read_img), #暂时没用
]


