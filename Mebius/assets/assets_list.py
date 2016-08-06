#!/usr/bin/env python3
#coding:utf8
import django
import os
from Mebius import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mebius.settings")
django.setup()
from assets import models
def fetch_asset_list():
    asset_list = models.Asset.objects.all()
    data_list = []
    for obj in asset_list:
        if hasattr(obj,'server') or hasattr(obj,'networkdevice'):
            if obj.asset_type == 'server':
                data = {
                        'id': obj.id,
                        'name': obj.name,
                        'management_ip': obj.management_ip,
                        'sn': obj.sn,
                        'idc': None if not obj.idc else obj.idc.model.idc.name,
                        'business_unit': None if not obj.business_unit else obj.business_unit.name,
                        'os_release':obj.server.os_release,
                         'cpu_model' : None if not obj.cpu else obj.cpu.cpu_model,
                         'cpu_core_count' : None if not obj.cpu else obj.cpu.cpu_core_count,
                         'ram_size': sum([i.capacity if i.capacity else 0 for i in obj.ram_set.select_related()]),
                        'disk_size': sum([i.capacity if i.capacity else 0 for i in obj.disk_set.select_related()]),
                }
                print(data_list.append(data))
    return  data_list