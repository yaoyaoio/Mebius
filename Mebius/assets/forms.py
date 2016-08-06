#!/usr/bin/env python3
#coding:utf8
from assets import models
from django.forms import ModelForm
class IDCForm(ModelForm):
    class Meta:   #写一个原类
        model = models.IDC  #关联的表
        exclude = ()         #什么字段都显示
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            print(field_name)
            field = cls.base_fields[field_name]
            attr_dic = {'class':'form-control',
                        'placeholder':field.help_text,
                        }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)