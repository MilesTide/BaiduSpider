#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import multiprocessing
import urllib
from urllib.parse import urlencode
import ast
import requests
from bs4 import BeautifulSoup
import pymongo
import datetime
import time
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

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get_baidu_html(keys,page,proxy,count,date):
    while count>0:
        data={
            'wd': keys,
            'pn': page,
            'gpc':"stf=" + yesterday + "," + now_time + "|stftype=1",
            'tfflag':1

        }  #pn 页码，lm,一天内的数据
        url = starturl+urlencode(data)  #要访问的url
        print("访问路径为"+url)
        #proxy = get_proxy().get("proxy") #获取代理
        response = requests.get(url,headers=headers,proxies={"http": "http://{}".format(proxy)},allow_redirects=False)
        #print("网页为："+response.text)
        soup = BeautifulSoup(response.text,'lxml')
        tagdiv1 = soup.find(name='div',id="content_left")
        if tagdiv1 == "" or tagdiv1 == None:#没有获取到参数
            delete_proxy(proxy) #换代理
            print("tagdiv1为空")
            print("第"+str(6-count)+"重新加载")
            count = count - 1
            proxy = get_proxy().get("proxy")  # 获取代理
            get_baidu_html(keys,page,proxy,count,date)  # 重新执行本方法，直到代理可用
        else:#顺利执行
            #print("顺利得到tagdiv1")
            print(tagdiv1)
            tagdiv2 = tagdiv1.find_all(name='div',attrs={"class":"result c-container"})
            if tagdiv2 != [] and tagdiv2 != None:#获取到参数
                #print("顺利得到tagdiv2")
                for divn in tagdiv2:
                    print(divn.get('id'))
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
                    htmldata={
                        'title':title,
                        'abstract':abstract,
                        'url':url,
                        'source':source,
                        'date':date
                    }
                    save_data(htmldata)
                    # print(divn.find('a').get('href'))
                    # print(divn.find(name='div',attrs={"class":"c-abstract"}).text)
                    # print(divn.find(name='div',attrs={"class":"f13 se_st_footer"}).text)
                    # print(divn.find(name='a', attrs={"target": "_blank"}).text)
                    #print(divn.text)
                    count=-1
                print("______________________page" + str(page / 10 + 1) + "_____________________________")
            else:#没有获取到参数，重新执行
                delete_proxy(proxy)  # 换代理
                print("tagdiv2为空")
                print("第" + str(6 - count) + "重新加载")
                count = count - 1
                proxy = get_proxy().get("proxy")  # 获取代理
                get_baidu_html(keys,page,proxy,count,date)  # 重新执行本方法，直到代理可用

def save_data(dict):
    date = str(datetime.date.today())
    client = pymongo.MongoClient('localhost', 27017)
    db = client['BaiduData']
    collection = db[date]
    collection.insert_one(dict)
    print("保存成功")

def main():
    keys1="量化 投资"
    keys2 = "量化 交易"
    date = str(datetime.date.today())
    #pool = multiprocessing.Pool(multiprocessing.cpu_count())#多线程

    pool = multiprocessing.Pool(4)
    count = 5#重新执行的次数
    proxy = get_proxy().get("proxy")  # 获取代理
    for i in range(1,11):
         result1 = pool.apply(get_baidu_html, (keys1,(i-1)*10,proxy,count,date))  # 多进程,最后一个参数是重试的次数，阻塞运行
         result2 = pool.apply(get_baidu_html, (keys2, (i - 1) * 10, proxy, count, date))
    pool.close()
    pool.join()
    print("爬取结束")

    # proxy = None  # 获取代理
    # count = 3  # 重新执行的次数
    # for i in range(1, 11):
    #     get_baidu_html(keys,(i-1)*10,proxy,count,date)
    # print("爬取成功")


if __name__ =="__main__":
    main()

