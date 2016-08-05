#!/usr/bin/env python3
#coding:utf8
from django.conf.urls import url
from member import views
urlpatterns = [
    url(r'^group/$', views.group,name='group',),
    url(r'^user/$', views.user,name='user',),
    url(r'^(\w+)/adds/', views.adds,name='adds',),
    url(r'^compiles/(\w+)/(\d+)/', views.compiles,name='compiles',),
    url(r'^userdetail/(\d+)/', views.userdetail,name='userdetail',),
    url(r'^deletes/', views.deletes,name='deletes',),
]
