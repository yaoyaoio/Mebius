from django.contrib import admin

# Register your models here
from assets import  models

#服务类型反向关联资产 所有使用这种方式
class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    readonly_fields = ['create_date']
#服务类型反向关联资产 所有使用这种方式
class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']
#服务类型反向关联资产 所有使用这种方式
class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']

class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']
class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','asset_type','name','sn','manufactory','model','management_ip','business_unit','idc')
    #把反向关联自己的表都显示出来
    inlines = [ServerInline,CPUInline,RAMInline,DiskInline,NICInline,]
    search_fields = ['sn',]
#资产
admin.site.register(models.Asset,AssetAdmin)

class CPUadmin(admin.ModelAdmin):
    list_display =('cpu_model','cpu_count','cpu_core_count','memo')
#cpu
admin.site.register(models.CPU,CPUadmin)
class NICadmin(admin.ModelAdmin):
    list_display =('name','sn','model','macaddress','ipaddress')
#网卡
admin.site.register(models.NIC,NICadmin)
#raid
admin.site.register(models.RaidAdaptor)
#内存
admin.site.register(models.RAM)
#IP
#硬盘
admin.site.register(models.Disk)

#设备厂商
admin.site.register(models.Manufactory)
#
#标签
admin.site.register(models.Tags)
#网络设备
admin.site.register(models.NetworkDevice)
#服务
admin.site.register(models.Server)
#系统or软件
admin.site.register(models.Software)
#业务线
admin.site.register(models.BusinessUnit)


#模块
class MoudleInline(admin.TabularInline):
    model = models.Moudle
    extra = 2
    exclude = ('memo',)

class CabinetInline(admin.TabularInline):
    model = models.Cabinet
    exclude = ('memo',)
#机房
class IdcAdmin(admin.ModelAdmin):

    list_display = ('name','contacts','idc_phone','idc_addr','contract','operator','memo')
    inlines = [MoudleInline,]
#机房表
admin.site.register(models.IDC,IdcAdmin)
#机房模块
admin.site.register(models.Moudle)
#机柜表
admin.site.register(models.Cabinet)
#运营商
admin.site.register(models.Operator)
#合同
admin.site.register(models.Contract)
