#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao

import scrapy
from scrapy.selector import Selector
import re
import time
class stan_24h():
    def __init__(self):
        self.COUN = [{}]

def pmchart(i,all_code):
    if i == 0:
        startnum = all_code.rfind('series :')
        endnum = all_code.rfind(' // 为echarts对象加载数据')
        pm24_data = re.findall("data:[^\s]*", all_code[startnum:endnum])
        return pm24_data
    elif i == 1 :
        startnum = all_code.find('series :')
        endnum = all_code.find(' // 为echarts对象加载数据')
        pm30_data = re.findall("data:[^\s]*", all_code[startnum:endnum])
        return pm30_data
    else:
        return False

def addpm242self(numlist,mon,day,hour):
    i = 0
    coun = [{}]
    for num in numlist:
        if hour == 24:
            hour = 0
            day = day+1
        else:
            pass
        coun += [{str(mon)+'-'+str(day)+'-'+str(hour):num}]
        i = i+1
        hour = hour+1
    coun = coun[1:]
    return coun

def addpm302self(numlist,year,mon,day):
    i = 29
    coun = [{}]
    n = []
    x = day
    y = 29
    while i >= 0:
       if i>=12:
           n.append(x)
           x = x-1
       else:
           n.append(y)
           y = y-1
       i = i-1
    for num in numlist:
        coun += [{n[i]:num}]
        i = i+1
    coun = coun[1:]
    return coun

class test_ajaxSpider(scrapy.Spider):
    name = "aajax"
    start_urls = ["http://www.pm25.com/city/beijing.html"]
    def parse(self, response):
        data = stan_24h()
        sel = Selector(response)
        print("**********************")
        all_code = response.text
        #提取24小时内和30小时内的data数据
        pm24_data = pmchart(0,all_code)
        pm30_data = pmchart(1,all_code)
        year =  int(time.strftime('%Y'))
        mon = int(time.strftime('%m'))
        day = int(time.strftime('%d'))
        hour = int(time.strftime('%H'))+1
        temp_c = 0
        #正则匹配提取每日pm2.5数据并创建列表
        while temp_c <=1:
            pm30temp = re.findall(r"\d+\.?\d*", pm24_data[temp_c])
            pm24temp = re.findall(r"\d+\.?\d*", pm30_data[temp_c])
            #调用函数生成结果列表
            if temp_c == 0:
                data.COUN[0] = addpm242self(pm24temp,mon,day-1,hour)
                data.COUN.append(addpm302self(pm30temp, mon, day, hour))
            else:
                data.COUN.append(addpm242self(pm24temp,mon,day-1,hour))
                data.COUN.append(addpm302self(pm30temp, mon, day, hour))
            temp_c = temp_c+1
        print('24h内美国标准：',data.COUN[0],'\n24h内中国标准：',data.COUN[2])
        print('30天内美国标准：', data.COUN[1], '\n30天内中国标准：', data.COUN[3])

if __name__ == "__main__":
    test_ajaxSpider()

