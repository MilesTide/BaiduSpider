#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import hashlib
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from pandas._libs import json
from requests import RequestException

max_behot_time = '0'  # 链接参数

def get_as_cp():  # 该函数主要是为了获取as和cp参数，程序参考今日头条中的加密js文件：home_4abea46.js
    zz = {}
    now = round(time.time())
    print(now)  # 获取当前计算机时间
    e = hex(int(now)).upper()[2:]  # hex()转换一个整数对象为16进制的字符串表示
    print('e:', e)
    a = hashlib.md5()  # hashlib.md5().hexdigest()创建hash对象并返回16进制结果
    print('a:', a)
    a.update(str(int(now)).encode('utf-8'))
    i = a.hexdigest().upper()
    print('i:', i)
    if len(e) != 8:
        zz = {'as': '479BB4B7254C150',
              'cp': '7E0AC8874BB0985'}
        return zz
    n = i[:5]
    a = i[-5:]
    r = ''
    s = ''
    for i in range(5):
        s = s + n[i] + e[i]
    for j in range(5):
        r = r + e[j + 3] + a[j]
    zz = {
        'as': 'A1' + s + e[-3:],
        'cp': e[0:3] + r + 'E1'
    }
    print('zz:', zz)
    return zz


def get_pageindex(url, headers, cookies):
    r = requests.get(url, headers=headers, cookies=cookies, verify=False)
    print(url)
    print(r.text)
    data = json.loads(r.text)
    print("_____________________data________________________")
    print(data)
    return data
def get_page(url, headers, cookies):
    try:
        r = requests.get(url, headers=headers, cookies=cookies, verify=False)
        print(type(r))
        demo2=r.text
        print("________demo2___________")
        print(demo2)
        if r.status_code == 200:
            print("success")
        print(url)
        return demo2
    except RequestException:
        print("请求失败")
def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    print("________________parse________________")
    #print(soup.p.contents)
    #for i,child in enumerate(soup.p.children):
     #   print(i,child.get_text())
    for p in soup.select('p'):
        print(p.get_text())

def main():
    source_url = []
    startrul = "https://www.toutiao.com"
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    cookies = {'tt_webid': '6649949084894053895'}  # 此处cookies可从浏览器中查找，为了避免被头条禁止爬虫
    ascp = get_as_cp()  # 获取as和cp参数的函数
    data={
    'category': 'stock',
    'utm_source': 'toutiao',
    'widen': 1,
    'max_behot_time': 0,
    'max_behot_time_tmp': 0,
    'tadrequire': 'true'
    }
    for i in range(5):
        url = "https://www.toutiao.com/api/pc/feed/?" + urlencode(data) + '&as=' + ascp['as'] + '&cp=' + ascp['cp']
        demo = get_pageindex(url,headers, cookies)
        print(len(demo))
        print(demo)
        for j in range(len(demo)):
            print("title:"+demo['data'][j]['title'])
            #print("abstract"+demo['data'][j]['abstract'])
            source_url.append(demo['data'][j]['source_url'])
        print(source_url)
        for k in range(len(demo)):
            print("_______________page__________________")
            print(k)
            url2 = startrul+source_url[k]
            print(url2)
            html= get_page(url2,headers,cookies)
            #print(html)
            #parse_page(html)



if __name__=="__main__":
       main()



