from django.shortcuts import render,HttpResponseRedirect,HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from assets import models
from assets import forms
from assets import assets_list
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger
from assets import core
import json
#资产列表
@login_required
def assetslist(request):
    assets = assets_list.fetch_asset_list()
    paginator = Paginator(assets,10)
    page = request.GET.get('page')
    try:
       assets_obj = paginator.page(page)
    except PageNotAnInteger:
       assets_obj = paginator.page(1)
    except EmptyPage:
       assets_obj = paginator.page(paginator.num_pages)
    return render(request,'assets/assetslist.html',{'assets':assets_obj})
#机房列表
@login_required
def assetsarea(request):
    idclist = models.IDC.objects.all()
    paginator = Paginator(idclist,10)
    page = request.GET.get('page')
    try:
        idclist_obj = paginator.page(page)
    except PageNotAnInteger:
        idclist_obj = paginator.page(1)
    except EmptyPage:
        idclist_obj = paginator.page(paginator.num_pages)
    return render(request,'assets/assetsarea.html',{'idclist':idclist_obj})

#模块列表
def modellist(request,func):
    pass
    return HttpResponseRedirect('/assets/assetsarea/')
#机柜列表
def cabinet(request,func):
    pass
    return HttpResponseRedirect('/assets/assetsarea/')
#网络设备列表
def netlist(request):
    return render(request,'assets/networklist.html')
#ip列表
def iplist(request):
    pass
    return HttpResponseRedirect('/assets/assetsarea/')
#机房相关资产
def idcasset(request):
    pass
    return HttpResponseRedirect('/assets/assetsarea/')
#添加机房功能
@login_required
def addarea(request):
    form = forms.IDCForm()
    if request.method == 'POST':
        form = forms.IDCForm(request.POST,request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            new_article_obj = models.IDC(**form_data)
            new_article_obj.save()
            return HttpResponseRedirect('/assets/assetsarea/')
    return render(request,'assets/addarea.html',{'formidc':form})
#编辑机房功能
@login_required
def compiles_area(request,func):
    obj = models.IDC.objects.get(id=int(func))
    if request.method == 'POST':
        formdata = forms.IDCForm(request.POST,instance=obj)
        if formdata.is_valid():
            formdata.save()
            return HttpResponseRedirect('/assets/assetsarea/')
    form = forms.IDCForm(instance=obj)
    if form.is_valid():
        form.save()
    return render(request,'assets/addarea.html',{'formidc':form})
#机房详细信息
@login_required
def roomdetail(request,func):
    if request.method == 'GET':
        obj = models.IDC.objects.get(id=func)
        return render(request,'assets/roomdetail.html',{'form':obj})
#服务器详细资产信息
@login_required
def hostdetail(request,func):
    if request.method == 'GET':
        print(type(func))
        obj = models.Asset.objects.get(id=func)
        return render(request,'assets/hostdetail.html',{'assets':obj})
#服务器更新功能
@login_required
def hostupdate(request):
    if request.method == 'POST':
        func = int(json.loads(request.POST.get('updateid')))
        if func:
            obj = models.Asset.objects.get(id=func)
            hostname = obj.name
            print(hostname)
            try:
                Asset = core.Assets(name=hostname)
                Asset.initialize()
                Asset.data_inject()
                return HttpResponse('ok')
            except:
                return HttpResponse('no')
