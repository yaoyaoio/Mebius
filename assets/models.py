from django.db import models

#导入用户
from member.models import UserProfile
#资产总表
class Asset(models.Model):
    asset_type_choices = (
        ('server', u'物理机'),
        ('server', u'虚拟机'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(verbose_name='资产类型',max_length=64,choices=asset_type_choices,default='server')
    name = models.CharField(max_length=64,unique=True)
    sn = models.CharField(u'资产SN号',max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory',verbose_name=u'制造商',null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP',blank=True,null=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同',null=True, blank=True)
    trade_date = models.DateField(u'购买时间',null=True, blank=True)
    expire_date = models.DateField(u'过保修期',null=True, blank=True)
    price = models.FloatField(u'价格',null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线',null=True, blank=True)
    #看看是哪个标签的
    tags = models.ManyToManyField('Tags' ,blank=True)
    admin = models.ForeignKey(UserProfile, verbose_name=u'资产管理员',null=True, blank=True)
    #每个资产都应该属于机柜 机柜属于模块 模块属于机房
    idc = models.ForeignKey('Cabinet', verbose_name=u'所属机柜',null=True, blank=True)
    Status_Status = (
        ('on','上线'),
        ('wait','等待上线'),
        ('in','下线'),
    )
    status = models.CharField(choices=Status_Status,max_length=64,verbose_name = u'设备状态',default=1)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    memo = models.TextField(u'备注', null=True, blank=True)
    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"
    def __str__(self):
        return 'id:%s name:%s'  %(self.id,self.name )


class Server(models.Model):
    asset = models.OneToOneField('Asset')
    created_by_choices = (
        ('auto','Auto'),
        ('manual','Manual'),
    )
    #手工添加还是自动添加
    created_by = models.CharField(choices=created_by_choices,max_length=32,default='auto')
    #如果是虚拟机 那么他的宿主机是这个
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    kernelrelease = models.CharField(u'内核',max_length=128,null=True, blank=True )
    #cpu 内存 网卡 raid卡 都是 这些关联他
    raid_type = models.CharField(u'raid级别',max_length=512, blank=True,null=True)
    os_type  = models.CharField(u'操作系统类型',max_length=64, blank=True,null=True)
    os_distribution =models.CharField(u'发型版本',max_length=64, blank=True,null=True)
    os_release  = models.CharField(u'操作系统版本',max_length=64, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
    def __str__(self):
        return '%s sn:%s' %(self.asset.name,self.asset.sn)

#网络设备
class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    vlan_ip = models.GenericIPAddressField(u'VlanIP',blank=True,null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP',blank=True,null=True)
    sn = models.CharField(u'SN号',max_length=128,unique=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True)
    port_num = models.SmallIntegerField(u'端口个数',null=True, blank=True)
    device_detail = models.TextField(u'设置详细配置',null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return  self.vlan_ip
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"

class Software(models.Model):
    '''
    软件和系统的管理 例如是买来的 有时间的。都可以通过这个记录
    '''
    os_types_choice = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('network_firmware', 'Network Firmware'),
        ('software', 'Softwares'),
    )
    type = models.CharField(u'系统类型', choices=os_types_choice, max_length=64,help_text=u'eg. GNU/Linux',default=1)
    distribution = models.CharField(u'发型版本',max_length=32)
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)
    language_choices = (('cn',u'中文'),
                        ('en',u'英文'))
    language = models.CharField(u'系统语言',choices = language_choices, default='cn',max_length=32)
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    def __str__(self):
        return self.version
    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"

class CPU(models.Model):
    '''
    CPU的基本类型
    '''
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128,blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    create_date = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新时间',blank=True,null=True)
    memo = models.TextField(u'备注', null=True,blank=True)
    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"
    def __str__(self):
        return self.cpu_model

class RAM(models.Model):
    '''
    内存条
    '''
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model =  models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'内存大小(MB)')
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    auto_create_fields = ['sn','slot','model','capacity']
    def __str__(self):
        return '%s:%s:%s' % (self.asset_id,self.slot,self.capacity)
    class Meta:
        verbose_name = '内存'
        verbose_name_plural = "内存"
        unique_together = ("asset", "slot")


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插槽位',max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice,default='SAS')
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    memo = models.TextField(u'备注', blank=True,null=True)
    auto_create_fields = ['sn','slot','manufactory','model','capacity','iface_type']
    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
    def __str__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id,self.slot,self.capacity)

#
class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True,null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    model =  models.CharField(u'网卡型号', max_length=128, blank=True,null=True)
    macaddress = models.CharField(u'MAC', max_length=64,unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True,null=True)
    netmask = models.CharField(verbose_name='子网掩码',max_length=64,blank=True,null=True)
    bonding = models.CharField(max_length=64,blank=True,null=True)
    memo = models.CharField(u'备注',max_length=128, blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    auto_create_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding']
    #auto_create_fields 定义这个表需要的数据 用于更新资产信息
    #我从例如json里 取出我这个表需要的key 之后插入到dataset里 取完之后插入到数据库里？
    def __str__(self):
        return '%s:%s' % (self.asset_id,self.macaddress)
    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"


class RaidAdaptor(models.Model):
    '''
    raid卡
    '''
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True,null=True)
    slot = models.CharField(u'插口',max_length=64)
    model = models.CharField(u'型号', max_length=64,blank=True,null=True)
    memo = models.TextField(u'备注', blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'raid卡'
        verbose_name_plural = 'raid卡'
        unique_together = ("asset", "slot")



class Manufactory(models.Model):
    '''
    资产的厂商名称和支持电话
    例如保修联系
    '''
    manufactory = models.CharField(u'厂商名称',max_length=64, unique=True)
    support_num = models.CharField(u'支持电话',max_length=30,blank=True)
    memo = models.CharField(u'备注',max_length=128,blank=True)

    def __str__(self):
        return self.manufactory
    class Meta:
        verbose_name = '设备厂商'
        verbose_name_plural = "设备厂商"

#机房模块表
class Moudle(models.Model):
    idc = models.ForeignKey('IDC',verbose_name='属于')
    name = models.CharField(u'机房模块',max_length=64,unique=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '机房模块'
        verbose_name_plural = "机房模块"

#机柜表
class Cabinet(models.Model):
    '''
    在机房一般机柜都是关联模块的 模块就是指这个机柜在机房哪个区
    因为机柜可以没有IP,所以没有关联IP 等着被IP关联 因为IP属于交换机的一部分 交换机属于机柜
    '''
    model = models.ForeignKey('Moudle',verbose_name='所属模块')
    name = models.CharField('机柜名称',max_length=64)
    quantity = models.CharField('电量',max_length=64)
    first_port = models.IntegerField('上联端口')
    bandwidth = models.CharField('带宽',max_length=64)
    put_position_choice = (
        ('forward', '正向摆放'),
        ('reverse','反向摆放'),
    )
    put_position = models.CharField('摆放规则',choices=put_position_choice,default='reverse',max_length=64)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __str__(self):
        return  self.name
    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = '机柜'
#机房表
class IDC(models.Model):
    '''
    机房表结构 关联合同和运营商
    机房表需要机房联系人 联系电话 机房的基本信息等
    '''
    name = models.CharField(u'机房名称',max_length=64,unique=True)
    contacts = models.CharField('机房技术',max_length=63)
    idc_phone = models.IntegerField('机房电话')
    contacts_phone = models.IntegerField('联系人电话')
    contacts_qq = models.IntegerField('机房技术QQ')
    idc_addr = models.CharField('机房地址',max_length=63)
    bandwidth = models.CharField('机房带宽',max_length=63)
    #关联合同
    contract = models.OneToOneField('Contract', verbose_name=u'合同',null=True, blank=True)
    #关联运营商
    operator = models.ForeignKey('Operator',verbose_name=u'运营商',null=True, blank=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"

#业务线
class BusinessUnit(models.Model):
    '''
        #自己关联自己 也许是二级业务线
    等着被关联
    '''
    parent_unit = models.ForeignKey('self',related_name='parent_level',blank=True,null=True)
    name = models.CharField(u'业务线',max_length=64, unique=True)
    memo = models.CharField(u'备注',max_length=64, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"
#合同
class Contract(models.Model):
    '''
    合同表  被机房关联
    '''
    sn = models.CharField(u'合同号', max_length=128,unique=True)
    name = models.CharField(u'合同名称', max_length=64 )
    price = models.IntegerField(u'合同金额')
    detail = models.TextField(u'合同详细',blank=True,null=True)
    #开始时间
    start_date = models.DateField(blank=True)
    #结束时间
    end_date = models.DateField(blank=True)
    file = models.FileField(upload_to='uploads/contract',verbose_name='合同文件')
    #不知道这个是干啥的。
    # license_num = models.IntegerField(u'license数量',blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date= models.DateField(auto_now=True)
    memo = models.TextField(u'备注', blank=True,null=True)
    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"
    def __str__(self):
        return self.name
#运营商
class Operator(models.Model):
    '''
    运营商表   例如：电信 联通 教育网 长城宽带等
    被机房关联。本身不关联任何表 只记录
    '''
    name = models.CharField(u'运营商',max_length=64,unique=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '运营商'
        verbose_name_plural = "运营商"
#标签
class  Tags(models.Model):
    '''
    此表是用来给资产贴标签使用的。
    '''
    #标签名
    name = models.CharField('Tag name',max_length=32, unique=True)
    #创建者
    creater = models.ForeignKey(UserProfile)
    #创建时间
    create_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"