#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import pymongo
import datetime
def save_data(dict):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['dbtest']
    collection = db['dbtestset']
    collection.insert_one(dict)
    print("保存成功")
def find_data():
    #连接mongodb 连接要操作的数据库  连接数据列表   增删改查操作
    date = str(datetime.date.today())
    client = pymongo.MongoClient('localhost', 27017)
    db = client['BaiduData']
    collection = db[date]
    #data=dbset.find({'age':20})
    data = collection.find()
    data1 = collection.find_one({'age':20})
    for exp in data:
        print(exp)
    #print(data1)
    print("查询成功")
def delete():
    date = str(datetime.date.today())
    client = pymongo.MongoClient('localhost', 27017)
    db = client['BaiduData']
    dbset = db[date]
    dbset.delete_many({'date':date})
    print('删除成功')
def updata():
    client = pymongo.MongoClient('localhost',27017)
    db = client['dbtest']
    dbset = db['detestset']
    dbset.update_one({'name':'王五'},{'$set':{'date': str(date)}})
    print("更新成功")
if __name__=="__main__":
    date = str(datetime.date.today())
    dict={
        'name':'张三',
        'age':20,
        'url':'www.baidu.com',
        'date': str(date)
    }
    #save_data(dict)
    delete()
    #updata()
    find_data()