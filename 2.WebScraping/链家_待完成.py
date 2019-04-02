#!/usr/bin/python 2.7
# -*- coding=UTF-8 -*-
# 能爬取数据，但未写入文件或数据库
from bs4 import BeautifulSoup
import requests
import re
import time


def get_pagetext(url, dirc):
    web_data = requests.get(url)
    source = BeautifulSoup(web_data.text,'lxml')
    Loupannames = source.select('body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-name > a')
    Lopanprices = source.select('body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-price > div.main-price > span.number')
    data = {}
    for name,price in zip(Loupannames,Lopanprices):
        SingleURL='https://cq.fang.lianjia.com' + name['href'] + 'xiangqing/'
        score = get_url_text(SingleURL)  #获取详细信息
        price_value = price.string
        if price_value == '价格待定':
            pass
        elif int(price_value) < 2000:
            justifyURL = 'https://cq.fang.lianjia.com' + name['href']
            price_value = justify_price(justifyURL)
        data={
            "name": name.string,
            "price": price_value,
            "score" : score
        }
        print(list(data.values()))

#核对单价
def justify_price(justifyURL):
    j_webdata = requests.get(justifyURL)
    j_soup = BeautifulSoup(j_webdata.text, "lxml")
    try:
        j_price = j_soup.select('#house-online > div > div.houselist > ul > li.info-li > p.p2 > span')[0].string
        j_area = j_soup.select('#house-online > div > div.houselist > ul > li.info-li > p.p1 > span')[0].string
        j_area = re.findall("\d+", j_area)[0]
        relprice = int(j_price) / int(j_area) * 10000
        relprice = int(relprice)
        return relprice
    except:
        print('这个楼盘暂无价格')
        return '价格待定'


#获取详细信息
def get_url_text(SingleURL):
    single_web_data = requests.get(SingleURL)
    single_source = BeautifulSoup(single_web_data.text, 'lxml')
    kinds = single_source.select('body > div.add-panel.clear > div.big-left.fl > ul > li > span.label-val')[0].string
    return kinds


#get pagesURL
def main_function():
    print("开始下载.....")
    for i in range(100):
        url = 'https://cq.fang.lianjia.com/loupan/pg%s'%str(i+1)
        get_pagetext(url,dirc1)
        print("第%s页下载完毕"%str(i+1))
        time.sleep(1) #时间保护


# main function
dirc1 = "D:\\book"           #储存位置
main_function()

