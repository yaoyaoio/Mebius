#!/usr/bin/env python3
#coding:utf8

from member import models
from django.forms import ModelForm
class UserForm(ModelForm):
    class Meta:   #写一个原类
        model = models.UserProfile  #关联的表
        exclude = ()         #什么字段都显示
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            if field_name == 'head_img':
                field = cls.base_fields[field_name]
                pass
            else:
                field = cls.base_fields[field_name]
                attr_dic = {'class':'form-control',
                            'placeholder':field.help_text,
                            }
                field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)
class GroupForm(ModelForm):
    class Meta:   #写一个原类
        model = models.Group  #关联的表
        exclude = ()         #什么字段都显示
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class':'form-control',
                        'placeholder':field.help_text,
                        }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)
