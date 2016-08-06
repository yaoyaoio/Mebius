from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from logs import models
from common import core
import time
# Create your views here.
@login_required
def index(request):
    info = core.info
    return render(request, 'common/index.html',{'info':info})
def ac_login(request):
    #登录功能
    if request.method == 'POST':
        #根据django自带的用户认证取出数据
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            #使用自带认证登录
            login(request,user)
            #登录成功返回首页
            username = request.POST.get('username')
            return HttpResponseRedirect('/')
        else:
            #登录失败
            login_err = "Wrong username or password!"
            #返回错误消息
            return render(request, 'common/login.html', {'login_err':login_err})
    #如果是get
    return render(request, 'common/login.html')
#退出返回登录页
def ac_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
