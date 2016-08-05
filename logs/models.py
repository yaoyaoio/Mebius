from django.db import models

from member.models import UserProfile
from assets.models import Asset

# Create your models here.
class EventLog(models.Model):
    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1,u'硬件变更'),
        (2,u'新增配件'),
        (3,u'设备下线'),
        (4,u'设备上线'),
        (5,u'定期维护'),
        (6,u'业务上线\更新\变更'),
        (7,u'其它'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices= event_type_choices)
    asset = models.ForeignKey('assets.Asset')
    component = models.CharField('事件子项',max_length=255, blank=True,null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间',auto_now_add=True)
    user = models.ForeignKey(UserProfile,verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '资产事件纪录'
        verbose_name_plural = "资产事件纪录"
    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.event_type == 2 :
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_event_type_display()
    colored_event_type.allow_tags = True
    colored_event_type.short_description = u'事件类型'


class UserLoginLog(models.Model):
    name = models.ForeignKey(UserProfile,verbose_name='用户')
    login = models.DateField('上次登录时间',auto_now=True)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name = '用户登录纪录'
        verbose_name_plural = '用户登录纪录'







class OperationLog(models.Model):
    '''
    用户远程管理 执行命令 分发文件日志管理
    '''
    name = models.CharField(u'操作名称', max_length=100)
    event_type_choices = (
        (1,u'执行命令'),
        (2,u'分发文件'),
        (3,u'服务部署'),
        (4,u'用户管理'),
        (5,u'部门管理'),
    )
    event_type = models.SmallIntegerField(u'操作类型', choices= event_type_choices)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间',auto_now_add=True)
    user = models.ForeignKey('member.UserProfile',verbose_name=u'操作人')
    memo = models.TextField(u'备注', blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '用户操作纪录'
        verbose_name_plural = '用户操作纪录'

