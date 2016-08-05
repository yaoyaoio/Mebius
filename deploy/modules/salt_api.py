# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import json
import os
class SaltAPI(object):
    #默认为空 tokenid
    __token_id = ''
    data = {}
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
    def token_id(self):
        ''' user login and get token id

        curl -k https://ip地址:8080/login
        -H "Accept: application/x-yaml" -d username='用户名' -d password='密码' -d eauth='pam'
        '''
        #获取token_id的请求数据
        params = {'eauth': 'pam', 'username': self.__user,'password': self.__password}
        #将请求的类型转成例如
        #password=salt&eauth=pam&username=salt
        encode = urllib.parse.urlencode(params)
        #转成二进制
        obj = encode.encode()
        #将二进制数据交给postRequest函数处理
        content = self.postRequest(obj,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
                raise KeyError
    def postRequest(self,obj,prefix="/"):
        #将url和后面的地址进行拼接
        url = self.__url + prefix
        # headers = {'X-Auth-Token': self.__token_id,'Accept':'application/json'}
        headers = {'X-Auth-Token': self.__token_id}
        #提交请求
        req = urllib.request.Request(url,obj,headers)
        response = urllib.request.urlopen(req)
        #获取结果
        request = response.read()
        #转成字典
        content = json.loads(str(request,encoding='utf-8'))
        return content
    def all_key(self):
        '''
        获取所有的minion_key
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # 取出认证已经通过的
        minions = content['return'][0]['data']['return']['minions']
        #print('已认证',minions)
        # 取出未通过认证的
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        # print('未认证',minions_pre)
        return minions,minions_pre

    #接受认证方法
    def accept_key(self,node_name):
        '''
        如果你想认证某个主机 那么调用此方法
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match':node_name}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    #删除认证方法
    def delete_key(self,node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret
    def remote_execution_module(self,tgt,fun):
        ''' tgt是主机 fun是模块
            写上模块名 返回 可以用来调用基本的资产
            例如 curl -k https://ip地址:8080/ \
        >      -H "Accept: application/x-yaml" \
        >      -H "X-Auth-Token:b50e90485615309de0d83132cece2906f6193e43" \
        >      -d client='local' \
        >      -d tgt='*' \
        >      -d fun='test.ping'  要执行的模块
        return:
        - iZ28r91y66hZ: true
          node2.minion: true
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret
    def remote_execution_func(self,tgt,fun,arg):
        '''
        #   curl -k https://ip地址:8080 \
        -H "Accept: application/x-yaml"
        -H "X-Auth-Token:b50e90485615309de0d83132cece2906f6193e43"
        -d client='local'
        -d tgt='*'            tgt是minion名称 默认匹配所有  如果加上 那么匹配固定主机名  这个函数可以用来获取硬件信息
        -d fun='grains.item'  使用grains.item模块
        -d arg='id'           查到主机的minionid
        return:
        - iZ28r91y66hZ:
            id: iZ28r91y66hZ
          node2.minion:
            id: node2.minion
        带参数
         curl -k http://115.29.51.8:8080/ -H "Accept: application/x-yaml"
          -H "X-Auth-Token: e5c2aa981109330ab9dacf238fb0ea0507d204cb"
          -d client='local' -d tgt='*'  -d fun='saltutil.sync_all'
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret
        #基于分组来执行
    def target_remote_execution(self,tgt,fun,arg):
        ''' 根据分组来执行 '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def server(self,tgt,arg):
        '''
        执行sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        return content
    def server_async(self,tgt,arg):
        '''异步sls '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
    def server_group(self,tgt,arg):
        ''' 分组进行sls '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        encode = urllib.parse.urlencode(params)
        obj = encode.encode()
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid
