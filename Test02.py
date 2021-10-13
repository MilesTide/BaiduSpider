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
    'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.100Safari / 537.36'
}
starturl="https://www.baidu.com/s?"
localway='F:\SpiderData'
proxypool_url = 'http://127.0.0.1:5555/random'
def get_proxy():
    return requests.get(proxypool_url).text.strip()

def get_baidu_html(key,page,proxy,count,date):
    while count>0:
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
        #print("网页为："+response.text)
        print(response.text)
        soup = BeautifulSoup(response.text,'lxml')
        tagdiv1 = soup.find(name='div',id="content_left")
        print(tagdiv1)
        if tagdiv1 == None:#没有获取到参数
            print("tagdiv1为空")
            print("第"+str(6-count)+"重新加载")
            count = count - 1
            proxy = get_proxy()  # 获取代理
            get_baidu_html(key,page,proxy,count,date)  # 重新执行本方法，直到代理可用
        else:#顺利执行
            #print("顺利得到tagdiv1")
            print(tagdiv1)
            tagdiv2 = tagdiv1.find_all(name='div',attrs={"class":"result c-container"})
            if tagdiv2 != [] or tagdiv2 != None:#获取到参数
                #print("顺利得到tagdiv2")
                for divn in tagdiv2:
                    id = key.replace(' ','')+str(divn.get('id'))
                    print(id)
                    data_inf = divn.find(name='div',attrs={"class":"c-tools"}).get('data-tools')
                    dict_data = ast.literal_eval(data_inf)
                    title = dict_data['title']
                    #abs = divn.find(name='div', attrs={"class": "c-abstract"}).text
                    doc = pq(str(divn))
                    doc.find('span').remove()
                    abstract= doc('.c-abstract').text()
                    url = dict_data['url']
                    source = divn.find(name='a', attrs={"class": "c-showurl"}).text
                    print(title)
                    print(abstract)
                    print(url)
                    print(source)
                    if RemoveDuplicates(abstract,title,source):
                        continue
                    htmldata={
                        '_id':id,
                        'title':title,
                        'abstract':abstract,
                        'url':url,
                        'source':source,
                        'date':date
                    }
                    try:
                        save_as_csv(htmldata,date)
                        save_data(htmldata, date)
                    except DuplicateKeyError:
                        print("重复写入")
                    count=-1
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
                dict['url'], dict['source'], dict['date']]
        writer = csv.writer(f)
        writer.writerow(text)
    print("保存csv成功")

def create_csv(date):
    filename=date+'.csv'
    fileway=os.path.join(localway,filename)
    with open(fileway,'w',newline='',encoding='utf-8-sig') as f:
        headers=['_id','title','abstract','url','source','date']
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
    keys =["量化 金融","量化 交易","量化 投资","量化 股票","量化 外汇","量化 代码","量化 期货"]
    date = str(datetime.date.today())
    pool = multiprocessing.Pool(4)
    count = 5#重新执行的次数
    proxy = get_proxy()  # 获取代理
    create_csv(date)
    for key in keys:
        for i in range(1,3):
             result = pool.apply(get_baidu_html, (key,(i-1)*50,proxy,count,date))  # 多进程,最后一个参数是重试的次数，阻塞运行
    pool.close()
    pool.join()
    print("爬取结束")

    # proxy = None  # 获取代理
    # count = 3  # 重新执行的次数
    # for i in range(1, 11):
    #     get_baidu_html(keys,(i-1)*50,proxy,count,date)
    # print("爬取成功")


if __name__ =="__main__":
    main()

