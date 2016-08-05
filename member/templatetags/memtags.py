#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
from django.utils.html import format_html
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()
#url剪切标签
@register.filter
def cut_url(img):
    try:
        url = img.name.split("/",maxsplit=1)[-1]
        return url
    except:
        return 1
@register.simple_tag
def gusee_page(current_page,loop_num):
    offset = abs(current_page - loop_num)
    if offset <5:
        if current_page == loop_num:
            page_ele = ''' <li class="paginate_button active"  aria-controls="editable" tabindex="0"><a class="page" href="?page=%s"  title="第%s页">%s</a></li>'''%(loop_num,loop_num,loop_num)
        else:
            page_ele = ''' <li class="paginate_button"  aria-controls="editable" tabindex="0"><a class="page" href="?page=%s"  title="第%s页">%s</a></li>'''%(loop_num,loop_num,loop_num)

        return format_html(page_ele)
    else:
        return ''
@register.filter
def pre(strpre):
    print(strpre)
    return 1