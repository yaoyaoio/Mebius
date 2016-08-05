#!/usr/bin/env python3
#coding:utf8
from django.conf.urls import url
from deploy import views
urlpatterns = [
    url(r'^salt_key', views.salt_key,name='salt_key',),
    url(r'^batchcmd', views.batchcmd,name='batchcmd',),
    url(r'^batchfile', views.batchfile,name='batchfile',),
    url(r'^remote', views.remote,name='remote',),
    url(r'^update', views.update,name='update',),
    url(r'^allowkey', views.allowkey,name='allowkey',),
    url(r'^deletekey', views.deletekey,name='deletekey',),
]
