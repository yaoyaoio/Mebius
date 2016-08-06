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
from django.conf.urls import url,include
from django.contrib import admin
from common import views
urlpatterns = [
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^$',views.index,name='index'),
    url(r'^login/$', views.ac_login,name='login',),
    url(r'^logout/$', views.ac_logout,name='logout',),
    url(r'^assets/', include('assets.urls')),
    url(r'^logs/', include('logs.urls')),
    url(r'^deploy/', include('deploy.urls')),
    url(r'^member/', include('member.urls')),
    url(r'^api/',include('api.rest_urls')),
]
