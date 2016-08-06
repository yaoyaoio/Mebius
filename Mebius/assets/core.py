# #!/usr/bin/env python3
# #coding:utf8
import django
import os
from Mebius import settings
from deploy.modules import salt_api
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mebius.settings")
django.setup()
from assets import models
# #获取资产信息
class Assets(object):
    def __init__(self,name=''):
        #主机名
        self.name = name
        #调用saltapi
        self.salt = salt_api.SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['username'], password=settings.SALT_API['password'])
        #获取资产硬件信息
        self.grains = self.salt.remote_execution_module(self.name,'grains.items')[self.name]
        print(self.grains)
        #定义一个基本资产包含的数据
        self.mandatory_fields = ['id','asset_id','asset_type']
        #定一个错误放置
        self.response = {
            'error':[],
            'info':[],
            'warning':[]
        }
    #一个错误信息的存放
    def response_msg(self,msg_type,key,msg):
        #判断有没有这个错误
        if self.response.get(msg_type):
            #如果没有追加
            self.response[msg_type].append({key:msg})
        else:
            return ValueError
    #数据监测提交data数据
    def __verify_field(self,data_set,field_key,data_type,required=True):
        '''
        data_set是资产数据
        field_key是key值
        data_type是类型
        :param data_set:
        :param field_key:
        :param data_type:
        :param required:
        :return:
        '''
        #print(data_set,field_key,data_type)
        #从数据中取出
        field_val = data_set.get(field_key)
        #如果有那么判断
        if field_val:
            try:
                #如果数据中的key 是字符串类型，那么判断结束
                data_set[field_key] = data_type(field_val)
            except ValueError as e:
                self.response_msg('error','无效的类型', "这个[%s]'s 的数据类型不正确 [%s] " % (field_key,data_type) )
        elif required == True:
                self.response_msg('error','数据不全', "这个 [%s] 不存在data数据中 [%s]" % (field_key,data_set) )

    #强制检测
    def mandatory_check(self,data,only_check_sn=False):
        for field in self.mandatory_fields:
            #如果不存在sn,asset_id,asset_type
            if not data.get(field):
                print('没有不存在')
                self.response_msg('error','强制检测错误', "这个 [%s] 没有提供数据" % field)
        else:
            #直接error并且返回
            if self.response['error']:return False
        try:
            #如果为true
            if not only_check_sn:
                #获取
                self.asset_obj = models.Asset.objects.get(id=int(data['asset_id']),name=data['id'])
                print(self.asset_obj)
            else:
                self.asset_obj = models.Asset.objects.get(name=data['id'])
                print(self.asset_obj)
            return True
        except ObjectDoesNotExist as e:
            self.response_msg('error','资产数据错误', "没有查到资产相关的%s和%s" % (data['asset_id'],data['sn']))
            self.waiting_approval = True
            return False
    def initialize(self):
        #取出资产信息
        data = self.grains
        # print(data)
        #判断资产数据是否存在
        if data:
            try:

                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'),name=data.get('id'),management_ip=data.get('fqdn_ip4')[0])
                #把这个服务的id设置为在数据库里自增的id
                data['asset_id'] = asset_obj[0].id
                #进行代码检测
                self.mandatory_check(data)
                #将检测成功后,执行
                self.clean_data = data
                #如果错误信息存放的地方没有error
                if not self.response['error']:
                    #返回为True
                    return True
            except ValueError as e:
                #错误信息
                self.response_msg('error','资产数据无效', str(e))
        else:
            self.response_msg('error','资产数据无效', "报告的资产数据是无效")
    #开始资产信息收录
    def data_inject(self):
        if self.__new_asset():
            print('这是一个新资产,开始创建')
            self.create_asset()
        else:
            print('这是一个旧资产,开始更新')
            self.update_asset()
    #判断是不是新的资产
    def __new_asset(self):
        #如果没有
        if not hasattr(self.asset_obj,self.clean_data['asset_type']):
            #开始创建资产
            return True
        else:
            return False
    #开始创建资产
    def create_asset(self):
        '''
        '''
        #经过函数找到_crate_方法 之后执行
        func = getattr(self,'_create_%s' % self.clean_data['asset_type'])
        create_obj =func()
    #开始更新资产
    def update_asset(self):
        func = getattr(self,'_update_%s' % self.clean_data['asset_type'])
        create_obj =func()
    #开始创建服务相关资产
    def _create_server(self):
        #基本服务信息
        self.__create_server_info()
        # #制造商信息
        self.__create_or_update_manufactory()
        # #cpu信息
        self.__create_cpu_component()
        # # #硬盘信息
        self.__create_disk_component()
        # # #网卡信息
        self.__create_nic_component()
        # # #内存信息
        self.__create_ram_component()
    #开始创建服务信息相关资产
    def __create_server_info(self,ignore_errs=False):
        try:
            #进行代码监测
            self.__verify_field(self.clean_data,'model',str)
            if not len(self.response['error']) or ignore_errs == True:
                data_set = {
                    'asset_id' : self.asset_obj.id,
                    'raid_type': self.clean_data.get('raid_type'),
                    'model':self.clean_data.get('model'),
                    'kernelrelease':self.clean_data.get('kernelrelease'),
                    'os_type':self.clean_data.get('os_type'),
                    'os_distribution':self.clean_data.get('os_distribution'),
                    'os_release':self.clean_data.get('os_release'),
                }
                print(data_set)
                #插入数据库
                obj = models.Server(**data_set)
                #保存
                obj.save()
                return obj
        except Exception as e:
            self.response_msg('error','对象创建异常','对象[server] %s' % str(e))
    #创建制造商例如kvm xen VMware
    def __create_or_update_manufactory(self,ignore_errs=False):
        try:
            #进行代码检测
            self.__verify_field(self.clean_data,'manufactory',str)
            #从数据里获取制造商信息
            manufactory = self.clean_data.get('manufactory')
            print(manufactory)
            if not len(self.response['error']) or ignore_errs == True:
                obj_exist = models.Manufactory.objects.filter(manufactory=manufactory)
                #判断这个制造商存在不存在
                if obj_exist:
                    obj = obj_exist[0]
                else:
                    #不存在插入
                    obj = models.Manufactory(manufactory=manufactory)
                    obj.save()
                self.asset_obj.manufactory = obj
                self.asset_obj.save()
        except Exception as e:
            self.response_msg('error','对象创建异常','Object [manufactory] %s' % str(e) )
    #获取cpu信息
    def __create_cpu_component(self,ignore_errs=False):
        try:
            self.__verify_field(self.clean_data,'model',str)
            self.__verify_field(self.clean_data,'cpu_count',int)
            self.__verify_field(self.clean_data,'cpu_core_count',int)
            if not len(self.response['error']) or ignore_errs == True:
                data_set = {
                    'asset_id' : self.asset_obj.id,
                    'cpu_model': self.clean_data.get('cpu_model'),
                    'cpu_count':self.clean_data.get('cpu_count'),
                    'cpu_core_count':self.clean_data.get('cpu_core_count'),
                }
                print(data_set)
                obj = models.CPU(**data_set)
                obj.save()
                log_msg = "Asset[%s] --> has added new [cpu] component with data [%s]" %(self.asset_obj,data_set)
                self.response_msg('info','NewComponentAdded',log_msg)
                return obj
        except Exception as e:
            self.response_msg('error','ObjectCreationException','Object [cpu] %s' % str(e) )
    #获取网卡信息
    def __create_nic_component(self):
        nic_info = self.clean_data.get('nic')
        if nic_info:
            for nic_item in nic_info:
                try:
                    self.__verify_field(nic_item,'macaddress',str)
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'name': nic_item.get('name'),
                            'sn': nic_item.get('sn'),
                            'macaddress':nic_item.get('macaddress'),
                            'ipaddress':nic_item.get('ipaddress'),
                            'bonding':nic_item.get('bonding'),
                            'model':nic_item.get('model'),
                            'netmask':nic_item.get('netmask'),
                        }
                        print(data_set)
                        obj = models.NIC(**data_set)
                        obj.save()

                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [nic] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','NIC info is not provied in your reporting data' )
    #获取内存信息
    def __create_ram_component(self):
        ram_info = self.clean_data.get('ram')
        if ram_info:
            print (ram_info)
            for ram_item in ram_info:
                try:
                    self.__verify_field(ram_item,'capacity',int)
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'slot': ram_item.get("slot"),
                            'sn': ram_item.get('sn'),
                            'capacity':ram_item.get('capacity'),
                            'model':ram_item.get('model'),
                        }
                        print(data_set)
                        obj = models.RAM(**data_set)
                        obj.save()

                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [ram] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','RAM info is not provied in your reporting data' )
    #获取硬盘信息
    def __create_disk_component(self):
        #获取硬盘信息目前不完善 只能获取sda 这种的和硬盘大小,暂时不能获取是否为ssd等信息
        disk_info = self.clean_data.get('physical_disk_driver')
        if disk_info:
            for disk_item in disk_info:
                try:
                    self.__verify_field(disk_item,'slot',str)
                    self.__verify_field(disk_item,'capacity',float)
                    # self.__verify_field(disk_item,'iface_type',str)
                    # self.__verify_field(disk_item,'model',str)
                    if not len(self.response['error']):
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            # 'sn': disk_item.get('sn'),
                            'slot':disk_item.get('slot'),
                            'capacity':disk_item.get('capacity'),
                            # 'model':disk_item.get('model'),
                            # 'iface_type':disk_item.get('iface_type'),
                            # 'manufactory':disk_item.get('manufactory'),
                        }
                        print(data_set)
                        obj = models.Disk(**data_set)
                        obj.save()
                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [disk] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','Disk info is not provied in your reporting data' )
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------资产更新----------------------------------------
    ##更新资产
    def _update_server(self):
        print('------------资产更新开始-----------')
        print('------------开始更新server信息-----------')
        server = self.__update_server_component(),
        print('------------开始更新CPU信息-----------')
        cpu = self.__update_cpu_component(),
        print('------------开始更新制造商信息-----------')
        manufactory = self.__update_manufactory_component(),
        nic = self.__update_asset_component(data_source=self.clean_data['nic'],
                                            fk='nic_set',
                                            update_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding'],
                                            identify_field = 'macaddress'
                                            ),
        ram = self.__update_asset_component(data_source=self.clean_data['ram'],
                                             fk='ram_set',
                                            update_fields = ['slot','sn','model','capacity'],
                                             identify_field = 'slot'
                                            ),
        print('开始资产收集硬盘信息-----------------------------------------------------')
        print('开始资产收集硬盘信息-----------------------------------------------------')
        print('开始资产收集硬盘信息-----------------------------------------------------')
        print('开始资产收集硬盘信息-----------------------------------------------------')
        print(self.clean_data['physical_disk_driver'])
        disk = self.__update_asset_component(data_source=self.clean_data['physical_disk_driver'],
                                             fk='disk_set',
                                             update_fields = ['slot','capacity'],
                                             identify_field = 'slot'
                                            ),
    #差集对比
    def __compare_componet(self,model_obj,fields_from_db,data_source):
        '''
        :param model_obj:
         server信息
        :param fields_from_db:
         要比较的字段
        :param data_source:
         收集过来的新数据
        :return:
        '''
        for field in fields_from_db:
            #从server数据库里面的取出旧的相关资产信息
            val_from_db = getattr(model_obj,field)
            # print(val_from_db)
            val_from_data_source = data_source.get(field)
            #从最新获取的信息里取出相关资产
            print(val_from_data_source)
            #判断是否存在
            if val_from_data_source:
                #将取出的资产进行类型比较并且转换类型
                if type(val_from_db) in (int,):
                    val_from_data_source = int(val_from_data_source)
                elif type(val_from_db) is float:
                    val_from_data_source = float(val_from_data_source)
                if val_from_db == val_from_data_source:
                    pass
                else:
                    #从表里查找找相关字段
                    #并且更新
                    db_field = model_obj._meta.get_field(field)
                    db_field.save_form_data(model_obj,val_from_data_source)
                    #记录更新时间
                    model_obj.update_date = timezone.now()
                    model_obj.save()
            else:
                self.response_msg('warning','资产更新警告',"资产组件(%s)的字段(%s)没有提供报告数据" % (model_obj,field) )
        model_obj.save()
    #更新server资产信息
    def __update_server_component(self):
        update_fields = ['model','raid_type','os_type','os_distribution','os_release','kernelrelease',]
        print('开始更新server信息')
        if hasattr(self.asset_obj,'server'):
            print(self.asset_obj.server)
            self.__compare_componet(model_obj=self.asset_obj.server,
                                    fields_from_db=update_fields ,
                                    data_source=self.clean_data)
        else:
            self.__create_server_info(ignore_errs=True)
    #更新制造商信息
    def __update_manufactory_component(self):
        self.__create_or_update_manufactory(ignore_errs=True)
    #更新cpu信息
    def __update_cpu_component(self):
        update_fields = ['cpu_model','cpu_count','cpu_core_count']
        if hasattr(self.asset_obj,'cpu'):
            self.__compare_componet(model_obj=self.asset_obj.cpu,
                                    fields_from_db=update_fields,
                                    data_source=self.clean_data)
        else:
            self.__create_cpu_component(ignore_errs=True)

    def __update_asset_component(self,data_source,fk,update_fields,identify_field=None):
        '''
        data_source:这个组件从报告数据的数据源
        fk:使用哪个关键发现之间的联系主要资产obj和每个资产组件
        update_fields: 字段在数据库进行比较和更新
        identify_field:使用这个字段来标识每个组件的资产,如果设置为None,意味着只有使用资产id来识别
         '''
        try:
            component_obj = getattr(self.asset_obj,fk)
            if hasattr(component_obj,'select_related'):
                print(component_obj)
                objects_from_db = component_obj.select_related()
                for obj in objects_from_db:
                    key_field_data= getattr(obj,identify_field)
                    print(key_field_data)
        #             #使用这个key_field_data找到相关数据来源报告数据
                    if type(data_source) is list:
                        print('---------------------------------------资产更新报告',data_source)
                        for source_data_item  in data_source:
                            print('资产循环',source_data_item)
                            # print(source_data_item)
                            key_field_data_from_source_data = source_data_item.get(identify_field)
                            if key_field_data_from_source_data:
                                #找到匹配的源数据的组件,然后要在这个组件比较每个字段是否有任何改变更新
                                if key_field_data == key_field_data_from_source_data:
                                    self.__compare_componet(model_obj=obj,fields_from_db=update_fields,data_source=source_data_item)
                                    break
                                    ##必须打破ast,如果循环完成后,逻辑将适用于. .其他部分,然后你就会知道,没有源数据是通过使用这种key_field_data匹配,
                                    # 这意味着,这个项目从源数据缺乏,当硬件信息有变化的时候,它是有意义的。e。旅客:一个内存坏了,某人拿走了,那么这些数据就不会被报道在报道数据
                            else:
                                self.response_msg('warning','资产更新警告',"资产组件[%s]'s 关键字段 [%s] 没有提供报告数据" % (fk,identify_field) )
                        else:
                            pass
                            # self.response_msg("error","找不到任何匹配的源数据用%s的字段" %(key_field_data))
                    #如果是字典
                    elif type(data_source) is dict :
                        for key,source_data_item  in data_source.items():
                            key_field_data_from_source_data = source_data_item.get(identify_field)
                            if key_field_data_from_source_data:
                                #找到匹配的源数据的组件,然后要在这个组件比较每个字段是否有任何改变自去年更新
                                if key_field_data == key_field_data_from_source_data:
                                   self.__compare_componet(model_obj=obj,fields_from_db=update_fields,data_source=source_data_item)
                                   break
                                   #这个项目从源数据缺乏,当硬件信息有变化的时候,它是有意义的
                            else:
                                self.response_msg('warning','资产更新警告',"资产组件[%s]'s 关键字段 [%s] 没有提供报告数据" % (fk,identify_field) )

                        else:#找不到任何匹配,资产手动组件必须被打破或改变
                            print('#找不到任何匹配,资产手动组件%s必须被打破或改变'%(key_field_data) )
                    else:
                        print('必须做某事错,逻辑应该去这里。')
                ##比较数据库的所有组件和报告数据的数据源
                self.__filter_add_or_deleted_components(model_obj_name=component_obj.model._meta.object_name, data_from_db=objects_from_db,data_source=data_source,identify_field=identify_field)

            else:
                pass
        except ValueError as e:
            print('\033[41;1m%s\033[0m' % str(e) )
    def __filter_add_or_deleted_components(self,model_obj_name,data_from_db,data_source,identify_field):
        print(data_from_db,data_source,identify_field)
        data_source_key_list = [] #save all the idenified keys from client data,e.g: [macaddress1,macaddress2]
        if type(data_source) is list:
            for data in data_source:
                data_source_key_list.append(data.get(identify_field))
        elif type(data_source) is dict:
            for key,data in data_source.items():
                if data.get(identify_field):
                    data_source_key_list.append(data.get(identify_field))
                else:#workround for some component uses key as identified field e.g: ram
                    data_source_key_list.append(key)
        print('-->identify field [%s] from db  :',data_source_key_list)
        print('-->identify[%s] from data source:',[getattr(obj,identify_field) for obj in data_from_db] )

        data_source_key_list = set(data_source_key_list)
        data_identify_val_from_db = set([getattr(obj,identify_field) for obj in data_from_db])
        data_only_in_db= data_identify_val_from_db - data_source_key_list #delete all this from db
        data_only_in_data_source=  data_source_key_list - data_identify_val_from_db #add into db
        print('\033[31;1mdata_only_in_db:\033[0m' ,data_only_in_db)
        print('\033[31;1mdata_only_in_data source:\033[0m' ,data_only_in_data_source)
        self.__delete_components(all_components=data_from_db, delete_list = data_only_in_db, identify_field=identify_field )
        if data_only_in_data_source:
            self.__add_components(model_obj_name=model_obj_name,all_components=data_source, add_list = data_only_in_data_source, identify_field=identify_field )

    def __add_components(self,model_obj_name,all_components,add_list,identify_field ):
        model_class = getattr(models,model_obj_name)
        will_be_creating_list = []
        print('--add component list:',add_list)
        if type(all_components) is list:
            for data in all_components:
                if data[identify_field] in add_list:
                    #print data
                    will_be_creating_list.append(data)
        elif type(all_components) is dict:
            for k,data in all_components.items():
                if data.get(identify_field):
                    if data[identify_field]  in add_list:
                        #print k,data
                        will_be_creating_list.append(data)
                else: #if the identified field cannot be found from data set,then try to compare the dict key
                    if k in add_list:
                        data[identify_field] = k #add this key into dict , because this dict will be used to create new component item in DB
                        will_be_creating_list.append(data)
        try:
            for component in will_be_creating_list:
                data_set = {}
                for field in model_class.auto_create_fields:
                    data_set[field] = component.get(field)
                data_set['asset_id'] = self.asset_obj.id
                obj= model_class(**data_set)
                obj.save()
                print('\033[32;1mCreated component with data:\033[0m', data_set)
                log_msg = "Asset[%s] --> component[%s] has justed added a new item [%s]" %(self.asset_obj,model_obj_name,data_set)
                self.response_msg('info','NewComponentAdded',log_msg)
        except Exception as e:
            print("\033[31;1m %s \033[0m"  % e )
            log_msg = "Asset[%s] --> component[%s] has error: %s" %(self.asset_obj,model_obj_name,str(e))
            self.response_msg('error',"AddingComponentException",log_msg)
    #删除资产部件
    def __delete_components(self,all_components, delete_list , identify_field ):
        '''All the objects in delete list will be deleted from DB'''
        deleting_obj_list = []
        print('--deleting components',delete_list,identify_field)
        for obj in all_components:
            val  = getattr(obj,identify_field)
            if val in delete_list:
                deleting_obj_list.append(obj)

        for i in deleting_obj_list:
            log_msg = "Asset[%s] --> component[%s] --> is lacking from reporting source data, assume it has been removed or replaced,will also delete it from DB" %(self.asset_obj,i)
            self.response_msg('info','HardwareChanges',log_msg)
            i.delete()

#
#
#
#
#
#
#
# #
# Asset = Assets(name='node1')
# #代码检测和创建基本数据库
# Asset.initialize()
# Asset.data_inject()
