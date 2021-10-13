#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao

from lxml import etree
import requests
from urllib import request

url = "http://www.baidu.com/"
req = request.Request(url)
response1 = request.urlopen(req)
html1 = etree.HTML(response1.read())
print("这个是response1: ", response1)  # 打印出response1是什么鬼
print("这个是type(response1: ", type(response1))  # 打印出response1的类型
print("这个是type(html1): ", type(html1))  # 打印html1的类型
print("这个是html1: ", html1)  # 打印出response1的用etree解析为html网页元素
# 打印网页的文本信息,由于这个response1只能调用一次所以这里会打印出空
print(response1.read().decode())  # 打印出网页源码的文本信息

print('*' * 70)

response2 = requests.get(url)
html2 = etree.HTML(response2.text)
print("这个是response2: ", response2)  # 打印出response2的内容
print("这个是type(response2): ", type(response2))  # 打印出response2的类型
print("这个是type(response2.text): ", type(response2.text))  # 打印出response2用text输出是的类型
print(type(response2.content.decode()))  # 打印出内容解码的类型
print("这个是type(html2): ", type(html2))  # 打印出response2用etree解析为网页元素信息的html2的类型
print("这个是html2 :", html2)  # 打印出response2用etree解析为网页元素信息的html2
# 打印网页的文本信息,用resquests有三种方法可以打印出网页的信息,这三种方法打印出来的都一样的
response2.encoding = 'utf-8'  # 给网页指定编码信息,是为了用text输出网页文本信息的
print(response2.text)  # 打印出网页的文本信息
print(response2.content.decode())  # 打印出网页源码的文本信息,这样写是为了避免出现中文乱码
print(str(response2.content, "utf-8"))  # 打印出网页源码的文本信息,这样写是为了避免出现中文乱码