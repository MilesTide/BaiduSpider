#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
html = '''<div class="c-abstract">
<span class=" newTimeFactor_before_abs  m">
3小时前&nbsp;-&nbsp;
</span>
比起80后、70后的私募基金经理,90后在
<em>量化投资</em>
私募领域风生水起,“年少多金”“技术男”“985毕业”是他们的醒目标签。而在主动投资私募阵营,80后、70...
</div>'''
print(type(html))
soup = BeautifulSoup(html,'lxml')
print(type(soup))
a= str(soup.find('div'))
doc = pq(a)
doc.find('span').remove()
print(doc.text())
#print(soup.find('span'))
#print(soup.text)