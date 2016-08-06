#!/usr/bin/env python3
#coding:utf8
from django.conf.urls import url,include
from rest_framework import routers
from api import rest_views

router = routers.DefaultRouter()
router.register(r'users',rest_views.UserViewSet)
router.register(r'assets',rest_views.AssetViewSet)
router.register(r'manufactories',rest_views.ManufactoryViewSet)

urlpatterns = [
    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]