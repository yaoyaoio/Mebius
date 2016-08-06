#!/usr/bin/env python3
#coding:utf8
import platform
import psutil
import django
import os
from Mebius import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mebius.settings")
django.setup()
from assets.models import Asset
from member.models import UserProfile
def TestPlatform():
    print ("----------Operation System--------------------------")
    #Windows will be : (32bit, WindowsPE)
    #Linux will be : (32bit, ELF)
    print(platform.architecture())
    #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
    #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
    print(platform.platform())
    #Windows will be : Windows
    #Linux will be : Linux
    print(platform.system())
    print ("--------------Python Version-------------------------")
    #Windows and Linux will be : 3.1.1 or 3.1.3
    print(platform.python_version())
def system():
  sysstr = platform.system()
  if(sysstr =="Windows"):
    return "windows"
  elif(sysstr == "Linux"):
    return "linux"
  else:
    return "other"
def resmem():
  mem = psutil.virtual_memory()
  return (str(int((mem.used/mem.total)*100)))
def rescpu(interval=1):
  return (str(psutil.cpu_percent(interval)))

def load_stat():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    loadavg['nr']=con[3]
    loadavg['last_pid']=con[4]
    return loadavg
asset = Asset.objects.count()
user = UserProfile.objects.count()
info = {'cpu':rescpu(),'mem':resmem(),'asset':asset,'user':user}