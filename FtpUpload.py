#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao

from ftplib import FTP  # 引入ftp模块
import os

ftp = FTP("ip")  # 设置ftp服务器地址
ftp.login('username', 'password')  # 设置登录账户和密码
ftp.retrlines('LIST')  # 列出文件目录
ftp.cwd('a')  # 选择操作目录
ftp.retrlines('LIST')  # 列出目录文件
localfile = '/mnt/NasFile/ftp测试/新功能.doc'  # 设定文件位置
f = open(localfile, 'rb')  # 打开文件
# file_name=os.path.split(localfile)[-1]
# ftp.storbinary('STOR %s'%file_name, f , 8192)
ftp.storbinary('STOR %s' % os.path.basename(localfile), f)  # 上传文件