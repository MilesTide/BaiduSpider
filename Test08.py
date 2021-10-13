#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import csv
import pandas as pd
import os
import multiprocessing
import urllib
from urllib.parse import urlencode
import ast
import requests
from bs4 import BeautifulSoup
import pymongo
import datetime
import time

from pymongo.errors import DuplicateKeyError
from pyquery import PyQuery as pq

now_time = str(int(time.time()))
yesterday = str(int(time.time()-24*60*60))
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}
starturl="https://www.baidu.com/s?"
localway='F:\SpiderData'
proxypool_url = 'http://127.0.0.1:5555/random'
def get_proxy():
    return requests.get(proxypool_url).text.strip()

def get_baidu_html(key,page,proxy,date):
    data={
        'wd': key,
        'rn':50,
        'pn': page,
        'gpc':"stf=" + yesterday + "," + now_time + "|stftype=1",
        'tfflag':1
    }                 #pn 页码，lm,一天内的数据
    url = starturl+urlencode(data)              #要访问的url
    print("访问路径为"+url)
    response = requests.get(url,headers=headers,proxies={'http': 'http://' + proxy},allow_redirects=False)
    response.raise_for_status()
    #response.encoding = response.apparent_encoding
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.text)
    tagdiv1 = soup.find_all(name="div",attrs={"class":"result c-container new-pmd"})
    #print(len(tagdiv1))
    for tag in tagdiv1:
        #print(tag)
        #print(tag.get('id'))
        id=tag.get('id')
        print(id)
        h3=tag.find(name="h3")
        title=h3.text
        link=h3.a.get('href')#这里是百度快照的地址，可以获得原地址，访问百度快照地址，获取头部信息
        req=requests.get(link,headers=headers,proxies={'http': 'http://' + proxy},allow_redirects=False)
        url=req.headers['location']
        #删除abstract中关于时间的记录
        doc = pq(str(tag))
        doc.find('span').remove()
        abstract = doc('.c-abstract').text()
        source = tag.find(name='a', attrs={"class": "c-showurl c-color-gray"}).text
        print(url)
        print(title)
        print(abstract)
        print(link)
        print(source)
        if RemoveDuplicates(abstract,title,source):
            continue
        htmldata={
            '_id':id,
            'title':title,
            'abstract':abstract,
            'url':url,
            'link': link,
            'source':source,
            'date':date
        }
        try:
            save_as_csv(htmldata,date)
            save_data(htmldata, date)
        except DuplicateKeyError:
            print("重复写入")
    print("______________________page" + str(page / 50 + 1) + "_____________________________")

def save_data(dict,date):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['BaiduData']
    collection = db[date]
    collection.insert_one(dict)
    print("保存成功")

def save_as_csv(dict,date):
    dict=dict
    filename=date+'.csv'
    fileway=os.path.join(localway,filename)
    #pd.DataFrame(dict).to_csv(fileway)
    with open(fileway,'a',newline='',encoding='utf-8-sig') as f:
        text = [dict['_id'], dict['title'], dict['abstract'],
                dict['url'],dict['link'], dict['source'], dict['date']]
        writer = csv.writer(f)
        writer.writerow(text)
    print("保存csv成功")

def create_csv(date):
    filename=date+'.csv'
    fileway=os.path.join(localway,filename)
    with open(fileway,'w',newline='',encoding='utf-8-sig') as f:
        headers=['_id','title','abstract','url','link','source','date']
        writer = csv.writer(f)
        writer.writerow(headers)
    print("创建成功")
def RemoveDuplicates(new_abs,new_title,new_source):
    #读取之前存储的内容，看是否有重复
    #没有重复返回0，有返回1
    #忽略百度贴吧内容
    if new_source=="百度贴吧":
        print("忽略此来源")
        return 1
    #读取存储的数据查重
    date = str(datetime.date.today())
    rootway = "F:\SpiderData"
    filename = date + '.csv'
    fileway = os.path.join(rootway, filename)
    data = pd.DataFrame(pd.read_csv(fileway, header=0))
    abstract = data['abstract'].values
    print(len(abstract))
    for i in range(len(abstract)):
        if abstract[i]==new_abs:
            print("词条重复"+abstract[i])
            return 1
    #分析摘要和标题中是否有敏感词
    import jieba
    jieba.load_userdict("newdict.txt")
    abandon = ['学院','招聘', '棋牌', '彩票', '下载','证书','实习','全职','转正','社招','校招','offer','留学','硕士','本科','教育','直播','APP','理财产品','天天基金网']
    cut=list(set(jieba.cut(new_abs)))
    cut2 = list(set(jieba.cut(new_title)))
    cut = cut+cut2
    for aban in abandon:
        for word in cut:
            if word==aban:
                print("有禁用词")
                return 1
    return 0

def main():
    import Mongodbtest
    Mongodbtest.delete()
    Mongodbtest.find_data()
    keys = ["量化 金融", "量化 交易", "量化 投资", "量化 股票", "量化 外汇", "量化 代码", "量化 期货"]
    date = str(datetime.date.today())
    #pool = multiprocessing.Pool(4)
    #count = 5  # 重新执行的次数
    proxy = get_proxy()  # 获取代理
    create_csv(date)
    for key in keys:
        for i in range(1, 3):
            get_baidu_html(key, (i - 1) * 50, proxy, date)
    #         pool.apply(get_baidu_html, (key, (i - 1) * 50, proxy, count, date))  # 多进程,最后一个参数是重试的次数，阻塞运行
    # pool.close()
    # pool.join()
    print("爬取结束")
    # key ="量化 金融"
    # date = str(datetime.date.today())
    # count = 5#重新执行的次数
    # proxy = get_proxy()  # 获取代理
    # result = get_baidu_html(key,0,proxy,count,date) # 多进程,最后一个参数是重试的次数，阻塞运行
    # print("爬取结束")

if __name__ =="__main__":
    main()

