from Mebius import settings
from deploy import models
from deploy.modules import salt_api
from assets.core import Assets
#获取minion端认证未认证的节点 之后获取他们IP 认证状态 写到数据库里
class Core(object):
    def __init__(self,name=''):
        self.salt = salt_api.SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['username'], password=settings.SALT_API['password'])
    def list_all_host(self):
        '''
        通过api获取所有认证和未认证的key列表
        之后取出插入到数据库
        之后教给前端展示
        写一个借口每次都从借口取出列表和数据库进行插集判断把改变的和没有的写入到数据库
        '''
        self.minions,self.minion_pre = self.salt.all_key()
    def authminions(self):
        for minion in self.minions:
            models.SaltMinion.objects.get_or_create(name=minion,status=1)
    def preminions(self):
        for pre in self.minion_pre:
            models.SaltMinion.objects.get_or_create(name=pre,status=2)
    def allow(self,name):
        print(name)
        print ('允许认证')
        self.salt.accept_key(name)
        print('认证后刷新grains')
        self.syncinfo(name=name)
    def delsalt(self,name):
        self.salt.delete_key(name)
    def syncinfo(self,name):
        obj = self.salt.remote_execution_module(tgt=name,fun='saltutil.sync_all')
        print ('obj--------------------------------------------------')
        print(obj)
        print('开始资产收集')
        Asset = Assets(name=name)
        Asset.initialize()
        Asset.data_inject()
    def saltcmd(self,name,func):
        obj = self.salt.remote_execution_func(tgt=name,fun='cmd.run',arg=func)
        return obj
    def server(self,func,arg):
        obj = self.salt.server(func,arg)
        return obj


























