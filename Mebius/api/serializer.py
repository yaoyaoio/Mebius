#!/usr/bin/env python3
#coding:utf8
from assets import models
from member.models import UserProfile
from rest_framework import  serializers,viewsets,routers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url','name','email','phone')
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        depth = 2
        fields = ('url','sn','asset_type','manufactory','name','create_date')
class ManfactorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Manufactory
        fields = ('url','manufactory','support_num','memo')