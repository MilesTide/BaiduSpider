#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @author: peidehao
from selenium import webdriver
import time
def get_index():
    browser = webdriver.Chrome()
    try:
        browser.get("https://www.toutiao.com/ch/stock_channel/")
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(100)
    finally:
        browser.close()

def main():
    get_index()

if __name__ =="__main__":
    main()
