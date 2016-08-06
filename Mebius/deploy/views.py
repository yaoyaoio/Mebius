from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,render_to_response,RequestContext
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger
from deploy import models
from deploy import core
import json
from logs.models import  OperationLog
# Create your views here.
@login_required
def salt_key(request):
    waitkey = core.Core()
    waitkey.list_all_host()
    waitkey.preminions()
    saltlist = models.SaltMinion.objects.all()
    paginator = Paginator(saltlist,10)
    page = request.GET.get('page')
    try:
        saltlist_objs = paginator.page(page)
    except PageNotAnInteger:
        saltlist_objs = paginator.page(1)
    except EmptyPage:
        saltlist_objs = paginator.page(paginator.num_pages)
    return render(request,'deploy/salt_key.html',{'saltlist_objs':saltlist_objs})
@login_required
def allowkey(request):
    if request.method == 'POST':
        Id = json.loads(request.POST.get('AllowId'))
        Hostname = json.loads(request.POST.get('AllowName'))
        print ('开始认证',Id,Hostname)
        allowcore = core.Core()
        allowcore.allow(Hostname)
        obj = models.SaltMinion.objects.get(id=int(Id),name=Hostname)
        obj.status = 1
        obj.save()
        objlogs = OperationLog.objects.create(name='允许认证',
                                                  event_type=4,
                                                  detail='认证主机%s'%(Hostname),
                                                  user_id=request.user.userprofile.id)
        return HttpResponse('ok')
    else:
        return HttpResponse('no')
@login_required
def deletekey(request):
    if request.method == 'POST':
        Id = json.loads(request.POST.get('DeleteId'))
        Hostname = json.loads(request.POST.get('DeleteName'))
        if models.SaltMinion.objects.filter(id=int(Id),name=Hostname):
            obj = models.SaltMinion.objects.filter(name=Hostname)
            obj.delete()
            deletecore = core.Core()
            deletecore.delsalt(Hostname)
            objlogs = OperationLog.objects.create(name='删除认证',
                                                  event_type=4,
                                                  detail='删除认证%s'%(Hostname),
                                                  user_id=request.user.userprofile.id)
            return HttpResponse(json.dumps('删除成功'))
        else:
            print('no')
    return HttpResponse('ok')
@login_required
def batchcmd(request):
    ret = ''
    if request.method  == 'POST':
        tgt = request.POST.get('tgt')
        arg = request.POST.get('arg')
        print (tgt,arg)
        if arg in ['rm -rf','rm']:
            ret = '不能执行rm 相关的命令 你老大会骂你的'
        else:
            saltcmd = core.Core()
            ret = saltcmd.saltcmd(tgt,arg)
            print(ret)
            objlogs = OperationLog.objects.create(name='命令执行',
                                                  event_type=4,
                                                  detail='针对：[%s]执行命令[%s]'%(tgt,arg),
                                                  user_id=request.user.userprofile.id)
    return render_to_response('deploy/batchcmd.html',
           {'ret':ret},context_instance=RequestContext(request))

@login_required
def batchfile(request):
    return render(request,'deploy/batchfile.html')
@login_required
def remote(request):
    if request.method  == 'POST':
        print(request.POST)
        tgt = request.POST.get('tgt')
        arg = request.POST.get('arg')
        saltserver = core.Core()
        saltserver.server(tgt,arg)
    return render(request,'deploy/remote.html')
@login_required
def update(request):
    return HttpResponse('更新认证列表成功')
