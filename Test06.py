#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import time
import datetime
import jieba

abandon = ['招聘','棋牌','彩票','游戏','下载']
abandon2 = ['veshi','jiau']
abandon = abandon+abandon2
#print(abandon)
jieba.load_userdict("newdict.txt")
juzi = "华商计算机行业量化股票型发起式证券投资基金招募说..._天天基金网"
ex = "作者:王倩 来源:《世界家苑》2018年第10期 摘要."
list1 = list(jieba.cut(juzi))
list2 = list(jieba.cut(ex))
list1 = list1+list2
for l in list1:
     print(l)