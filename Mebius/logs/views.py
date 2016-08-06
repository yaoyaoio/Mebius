from django.shortcuts import render
from logs import models
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def assetslogs(request):
    assetslog = models.EventLog.objects.all()
    paginator = Paginator(assetslog,10)
    page = request.GET.get('page')
    try:
        assetslog_objs = paginator.page(page)
    except PageNotAnInteger:
        assetslog_objs = paginator.page(1)
    except EmptyPage:
        assetslog_objs = paginator.page(paginator.num_pages)
    return render(request,'logs/assetslogs.html',{'assetslog_objs':assetslog_objs})

def executelogs(request):
    executelog = models.OperationLog.objects.all()
    paginator = Paginator(executelog,10)
    page = request.GET.get('page')
    try:
        executelog_objs = paginator.page(page)
    except PageNotAnInteger:
        executelog_objs = paginator.page(1)
    except EmptyPage:
        executelog_objs = paginator.page(paginator.num_pages)
    return render(request,'logs/executelogs.html',{'executelog_objs':executelog_objs})
def loginlogs(request):
    login = models.UserLoginLog.objects.all()
    return render(request,'logs/loginlogs.html',{'login':login})