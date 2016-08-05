"""Mebius URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from assets import views
urlpatterns = [
    #列表展示
    url(r'^assetslist$', views.assetslist,name='assetslist',),
    url(r'^assetsarea', views.assetsarea,name='assetsarea',),
    url(r'^netlist', views.netlist,name='netlist',),
    url(r'^iplist', views.iplist,name='iplist',),
    url(r'^modellist/(\d+)', views.modellist,name='modellist',),
    url(r'^cabinet/(\d+)', views.cabinet,name='cabinet',),
    url(r'^idcasset/(\d+)', views.idcasset,name='idcasset',),
    #添加
    url(r'^addarea', views.addarea,name='addarea',),
    #详细信息
    url(r'^hostdetail/(\d+)', views.hostdetail,name='hostdetail',),
    #服务器更新
    url(r'^hostupdate', views.hostupdate,name='hostupdate',),
    url(r'^roomdetail/(\d+)', views.roomdetail,name='roomdetail',),
    #编辑
    url(r'^compilesarea/(\d+)', views.compiles_area,name='compilesarea',),
]
