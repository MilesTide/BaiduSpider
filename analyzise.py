#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import re

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
def spiderlink(url):
    print(url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
    baidu_header = requests.get(url, headers=headers, allow_redirects=False)
    #百度快照不能直接爬取，但是百度快照链接的header中含有原链接信息
    real_url1 = baidu_header.headers['Location'] #获取原链接
    print(real_url1)
    response = requests.get(real_url1, headers=headers, allow_redirects=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find_all(attrs={'class': re.compile("\w*article$", re.I)})
    if article:
        for artc in article:
            Alltext = artc.find_all('p')#查找P标签里的所有文字，过滤掉含有a标签的内容，还有一些网站不在p标签内
            if Alltext:
                print("第一层")
                for p in Alltext:
                    if p.find('a'):
                        continue
                    print(p.text)
    else:
        #第二层查找real_url
        realhead = requests.get(real_url1, headers=headers, allow_redirects=False)
        realhead.encoding = 'utf-8'
        # 百度快照不能直接爬取，但是百度快照链接的header中含有原链接信息
        real_url = realhead.headers['Location']  # 获取原链接
        real_url = real_url+'/'
        print("第二层")
        print("真实地址" + real_url)
        response = requests.get(real_url, headers=headers, allow_redirects=False)
        #print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        article = soup.find_all(attrs={'class': re.compile("\w*article$", re.I)})
        if article:
            for artc in article:
                Alltext = artc.find_all('p')  # 查找P标签里的所有文字，过滤掉含有a标签的内容，还有一些网站不在p标签内
                if Alltext:
                    print("第一层")
                    for p in Alltext:
                        if p.find('a'):
                            continue
                        print(p.text)

if __name__=='__main__':
    count=0
    rootway="F:/TagData/2020-08-18.csv"
    df = pd.DataFrame(pd.read_csv(rootway))
    data = np.array(df)
    length = len(df)
    for i in range(length):
        if data[i][-1]==1:
            count = count+1
            print(count)
            url=str(data[i][2])
            spiderlink(url)

            # print(data[i][0])#title
            # print(data[i][1])#abstract
            # print(data[i][2])#link
            # print(data[i][3])#source
            # print(data[i][4])#tag

