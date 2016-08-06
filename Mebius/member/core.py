#!/usr/bin/env python3
#coding:utf8
import  os
#图片上传和文件上传函数
def upload_file_img(request,files):
    #文件上传路径
    base_img_upload_path = 'uploads/portrait'
    print(base_img_upload_path)
    # #指定用户上传路径 uploads/用户id/文件名
    # #判断是否存在用户路径
    # if not os.path.exists(base_img_upload_path):
    #     #不存在创建
    #     os.mkdir(base_img_upload_path)
    # #打开文件
    # with open("%s/%s" %(base_img_upload_path,files.name), 'wb+') as file_img:
    #     for chunk in files.chunks():
    #         file_img.write(chunk)
    # #返回url
    # return  "/%s" %(files.name)