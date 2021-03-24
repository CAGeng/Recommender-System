from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static 
from . import views
from django.views.static import serve

from django import urls
from django.conf.urls import url

urlpatterns = [
    path('getm/', view=views.get_movies),  #
    path('login/', view=views.login),
    path('images/', view=views.read_img),
]


