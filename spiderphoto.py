#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
import requests
import time
import os
from urllib import request
import re

#请求头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
			'referer': 'https://www.toutiao.com/search/?keyword=%E5%B0%8F%E5%A7%90%E5%A7%90',
			'cookie': 'tt_webid=6805093436782708238; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6805093436782708238; csrftoken=9412d118eebe20139b2180cdae95722d; ttcid=c90a8e8626874418add2469184072fe532; RT="z=1&dm=toutiao.com&si=z3bslifp08&ss=k800uaig&sl=9&tt=8xq&obo=5&ld=5qz1g&r=0f8c32692cd648ca8888f3a24ac0cb09&ul=5qz1j&hd=5qz1m"; SLARDAR_WEB_ID=56b7b4f5-3148-4239-bc72-d5f5f6c81e3e; s_v_web_id=verify_k818jznx_vJj3CICd_Vf4r_46br_8Gdr_uVv4NugWPaO3; __tasessionId=ii2wsjlel1584772377896; tt_scid=yCii1T2rQObu5AzeSWNNrDFm6WTNz0WPmTZ2Y69NPUH4h8Whdv6xA7XqozVxxrUAfba1'
			}
#获取时间戳
for i in range(20,101,20):
	timestamp = int(time.time()*1000)
	url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={j}&format=json&keyword=%E5%B0%8F%E5%A7%90%E5%A7%90&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp={k}&_signature=1yhIUgAgEBARf.HfQ988A9cpCUAAIlmWSLvbQsNnt7yIt.AP5xeQpTxPko6nwEQ9h8sOE7IAozHYcml6xPUSLt-1Pb6LULcx.yWCRAHV3n1QCweCpHLMXIxnR-4adJa3njy'.format(j=i,k=timestamp)
	#解码
	resp = requests.get(url,headers=headers).json()
	datas = resp['data']
	print('='*30)
	print('下载第%d页'%(i/20))
	for data in datas:
		try:
			#替换标题中的特殊符号和去掉空格
			title = re.sub(r'[\\/\:\*?<>\|]*','',data['title']).strip()
		except:
			continue
		#创建图片标题名对应的文件夹
		dir_path = os.path.join('test',title)
		if not os.path.exists(dir_path):
			os.mkdir(dir_path)
		try:
			for i,image in enumerate(data['image_list']):
				#将图片网址替换为大图网址
				url = re.sub(r'list/190x124|list','origin',image['url'])
				try:
					request.urlretrieve(url,os.path.join(dir_path,'%d.jpg'%(i+1)))
					print(title+' 第%d张图片下载成功'%(i+1))
				except:
					print(title+' 第%d张图片下载失败'%(i+1))
		except:
			pass