from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,update_last_login
# Create your models here.
class UserProfile(models.Model):
    '''
    用户表
    '''
    user = models.OneToOneField(User,verbose_name='后台用户')
    #名字
    name = models.CharField(max_length=32,verbose_name='姓名')
    #头像
    head_img = models.ImageField(blank=True,null=True,upload_to="uploads/portrait",verbose_name='头像')
    #邮箱
    email = models.EmailField(max_length=64,blank=True,null=True,verbose_name='邮箱')
    #手机号
    phone = models.CharField(verbose_name='手机号',max_length=128)
    #部门
    department = models.ForeignKey('Group',verbose_name='部门',null=True,blank=True)
    #公司ip
    ip = models.GenericIPAddressField(max_length=32,verbose_name='办公IP')
    #秘钥
    secret_key = models.TextField(verbose_name='密钥')
    #备注
    memo = models.TextField(verbose_name='备注', null=True, blank=True)
    #创建时间
    create_date  = models.DateField(verbose_name='注册时间',auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '成员'
        verbose_name_plural = '成员'
class Group(models.Model):
    #群组名称
    name = models.CharField(max_length=64,verbose_name='部门')
    #负责人
    owner = models.ForeignKey(UserProfile,verbose_name='负责人')
    #备注
    memo = models.TextField(u'备注', null=True, blank=True)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name='部门'
        verbose_name_plural = '部门'