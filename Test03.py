#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
# -*- coding:utf-8 -*-
'''
从百度把前10页的搜索到的url爬取保存
'''
import multiprocessing  # 利用pool进程池实现多进程并行
#  from threading import Thread 多线程
import time
from bs4 import BeautifulSoup  # 处理抓到的页面
import sys
import requests
import importlib

importlib.reload(sys)  # 编码转换，python3默认utf-8,一般不用加
from urllib import request
import urllib
from pymongo import MongoClient

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}  # 定义头文件，伪装成浏览器

urls =[]
def getfromBaidu(word):
    start = time.clock()
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote(word) + '&pn='  # word为关键词，pn是百度用来分页的..
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for k in range(1, 5):
        result = pool.apply_async(geturl, (url, k))  # 多进程
    pool.close()
    pool.join()
    end = time.clock()
    print(end - start)

def geturl(url, k):
    path = url + str((k - 1) * 10)
    response = request.urlopen(path)
    page = response.read()
    soup = BeautifulSoup(page, 'lxml')
    tagh3 = soup.find_all('h3')
    for h3 in tagh3:
        href = h3.find('a').get('href')
        # print(href)
        baidu_url = requests.get(url=href, headers=headers, allow_redirects=False)
        real_url = baidu_url.headers['Location']  # 得到网页原始地址
        if real_url.startswith('http'):
            urls.append(real_url)
    for url in urls:
        print(url)
        # all.write(real_url + '\n')


if __name__ == '__main__':
    getfromBaidu('周杰伦')
