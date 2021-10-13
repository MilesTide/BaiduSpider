#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import re

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
def spiderlink(baidu_url):
    print(url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
    baidu_url = requests.get(url, headers=headers, allow_redirects=False)
    #百度快照不能直接爬取，但是百度快照链接的header中含有原链接信息
    real_url = baidu_url.headers['Location'] #获取原链接
    print("真实地址"+real_url)
    response = requests.get(real_url, headers=headers, allow_redirects=False)
    response.encoding='utf-8'
    #print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    Alltext = soup.find_all('p')  # 查找P标签里的所有文字，过滤掉含有a标签的内容，还有一些网站不在p标签内
    if Alltext:
        print("第一层")
        for p in Alltext:
            print(p.text)
    #article = soup.find(attrs={"class": "article"})
    # article = soup.find(attrs={'class': re.compile("^article$", re.I)})
    # print(article.text)
if __name__=='__main__':
    url = 'https://zhuanlan.zhihu.com/p/183801371'#'http://www.baidu.com/link?url=9nNq5JpkGaHqqyHVTxiagw4uI63irU9vqsNjotbaLeikduBMBsEVO6K1ZaXMzAqAQcb0oNxzU0bhboj0SIN-C5L44vvvumCV9HIiErX95eK'#'http://futures.cnfol.com/mingjialunshi/20200819/28347203.shtml'#'http://www.douban.com/group/topic/190030632'#'https://k.sina.com.cn/article_2374263613_8d84633d00100rt8z.html'
    spiderlink(url)
    # rootway="F:/TagData/2020-08-20.csv"
    # df = pd.DataFrame(pd.read_csv(rootway))
    # data = np.array(df)
    # length = len(df)
    # for i in range(length):
    #     if data[i][-1]==1:
    #         url=str(data[i][2])
    #         spiderlink(url)

            # print(data[i][0])#title
            # print(data[i][1])#abstract
            # print(data[i][2])#link
            # print(data[i][3])#source
            # print(data[i][4])#tag

