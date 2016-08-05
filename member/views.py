from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import  Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
from member import models
from member import forms
from  logs.models import OperationLog
import json
@login_required
def group(request):
    grouplist = models.Group.objects.all()
    paginator = Paginator(grouplist,10)
    page = request.GET.get('page')
    try:
        grouplist_objs = paginator.page(page)
    except PageNotAnInteger:
        grouplist_objs = paginator.page(1)
    except EmptyPage:
        grouplist_objs = paginator.page(paginator.num_pages)
    return render(request,'member/group.html',{'grouplist_objs':grouplist_objs})
@login_required
def user(request):
    group = models.Group.objects.all()
    userlist = models.UserProfile.objects.all()
    #设置要显示的页面数量
    paginator = Paginator(userlist,10)
    page = request.GET.get('page')
    try:
        userlist_objs = paginator.page(page)
        print(userlist_objs)
    except PageNotAnInteger:
        #如果页面不是一个整数,交付第一页。
        userlist_objs = paginator.page(1)
    except EmptyPage:
        userlist_objs = paginator.page(paginator.num_pages)
    return render(request,'member/user.html',{'userlist_objs':userlist_objs,'group':group})
@login_required
#添加功能
def adds(request,func):
    if func == 'user':
        form = forms.UserForm()
        if request.method == 'POST':
            form = forms.UserForm(request.POST,request.FILES)
            if form.is_valid():
                form_data = form.cleaned_data
                new_article_obj = models.UserProfile(**form_data)
                new_article_obj.save()
                #日志记录
                obj = OperationLog.objects.create(name='添加用户',
                                                  event_type=4,
                                                  detail='添加用户%s'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
                return HttpResponseRedirect('/member/user/')
        return render(request, 'member/adds.html', {'form':form})
    elif func == 'group':
        form = forms.GroupForm()
        if request.method == 'POST':
            form = forms.GroupForm(request.POST,request.FILES)
            if form.is_valid():
                form_data = form.cleaned_data
                new_article_obj = models.Group(**form_data)
                new_article_obj.save()
                obj = OperationLog.objects.create(name='添加部门',
                                                  event_type=5,
                                                  detail='添加部门%s'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
                return HttpResponseRedirect('/member/group/')
        return render(request, 'member/adds.html', {'form':form})
    else:
        return HttpResponseRedirect('/member/user/')


@login_required
#编辑功能
def compiles(request,func,id):
    if func == 'group':
        obj = models.Group.objects.get(id=int(id))
        if request.method == 'POST':
            print(request.POST)
            formdata = forms.GroupForm(request.POST,instance=obj)
            print(formdata)
            if formdata.is_valid():
                formdata.save()
                obj = OperationLog.objects.create(name='修改部门',
                                                  event_type=5,
                                                  detail='修改部门%s信息'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
                return HttpResponseRedirect('/member/group/')
            else:
                return render(request, 'member/compile.html', {'form':formdata})
        # obj = models.Group.objects.get(id=int(id))
        form = forms.GroupForm(instance=obj)
        if form.is_valid():
            form.save()
        return render(request, 'member/compile.html', {'form':form})
    elif func == 'user':
        obj = models.UserProfile.objects.get(id=int(id))
        if request.method == 'POST':
            # request.POST = request.POST.copy()
            # from member import core
            # core.upload_file_img(request,request.FILES['head_img'])
            formdata = forms.UserForm(request.POST,request.FILES,instance=obj)
            if formdata.is_valid():
                formdata.save()
                obj = OperationLog.objects.create(name='修改用户',
                                                  event_type=4,
                                                  detail='修改用户%s信息'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
                return HttpResponseRedirect('/member/user/')
            else:
                return render(request, 'member/compile.html', {'form':formdata})
        form = forms.UserForm(instance=obj)
        if form.is_valid():
            form.save()
        return render(request, 'member/compile.html', {'form':form})
    else:
         return HttpResponseRedirect('/member/user/')
#删除用户或组操作
def deletes(request):
    Id = json.loads(request.POST.get('DeleteId'))
    name = json.loads(request.POST.get('DeleteName'))
    if name == 'group':
        obj = models.Group.objects.filter(id=int(Id)).delete()
        objlog = OperationLog.objects.create(name='删除部门',
                                                  event_type=5,
                                                  detail='删除部门%s'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
        return HttpResponse(json.dumps('ok'))
    elif name == 'user':
        obj = models.UserProfile.objects.filter(id=int(Id)).delete()
        objlog = OperationLog.objects.create(name='删除用户',
                                                  event_type=4,
                                                  detail='删除用户%s'%(request.POST['name']),
                                                  user_id=request.user.userprofile.id)
        return HttpResponse(json.dumps('ok'))

def userdetail(request,func):
    objuser = models.UserProfile.objects.get(id=func)
    return render(request,'member/userdetail.html',{'objuser':objuser})