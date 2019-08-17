# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import random
import re
import os


def get_result(ybcode, page=1):  # 数据的请求
    data = {'ybcode': ybcode, 'entrycode': '', 'page': page, 'pagerow': '20'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url = "http://data.cnki.net/Yearbook/PartialGetCatalogResult"
    params = urllib.parse.urlencode(data).encode(encoding='utf-8')
    req = urllib.request.Request(url, params, headers)
    r = urllib.request.urlopen(req)
    res = str(r.read(), 'utf-8')
    return res


def get_pageno(ybcode):  # 获取总页数
    soup = BeautifulSoup(get_result(ybcode), 'lxml')
    pages = int(soup.select('.s_p_listl')[0].get_text().split("共")[2].split('页')[0])
    print('总共' + str(pages) + '页')
    return pages


def dataclear(data):  # 数据的清理，除去文本中所有的\n和\r
    data = re.sub('\n+', ' ', data)
    data = re.sub('\r+', ' ', data)
    data = re.sub(' +', ' ', data)
    return data


def filedata(ybcode, year):  # 下载知网的统计年鉴之类的所有excel表
    pageno = get_pageno(ybcode)
    for i in range(1, pageno + 1, 1):
        print('########################################当前第' + str(i) + '页###################################')
        soup = BeautifulSoup(get_result(ybcode, i), 'lxml')
        for j in soup.select('tr'):
            s = BeautifulSoup(str(j), 'lxml')
            if len(s.select('img[src="/resources/design/images/nS_down2.png"]')) == 0:
                pass
            else:
                try:
                    if len(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a')) >= 2:
                        title = str(BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(1) > a')[0].get_text())
                        url = 'http://data.cnki.net' + BeautifulSoup(str(j), 'lxml').select('td:nth-of-type(3) > a')[1].get('href')
                        title = dataclear(title)  # 若不清洗数据，则文件名中会包含\n等特殊字符，导致文件下载错误
                        filedown(title, url, year)
                except Exception as e:
                    print('error:-------------------' + str(e))
                    pass


def filedown(title, url, year):  # 文件下载函数
    try:
        print(title,url,year,sep=" ")
        r = requests.get(url)

        # 创建文件夹
        folder = "D:\\年鉴数据下载"
        path = folder + '\\' + str(year)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)

        # 下载数据
        excelname = title + ".xls"
        with open(excelname, "wb") as code:
            code.write(r.content)
            print(path + '\\' + title + ".xls" + ' 下载完成')



    except Exception as e:
        print("error")
        pass
    x = random.randint(3, 4)
    time.sleep(x)


if __name__ == '__main__':
    # 默认下载到D盘的“年鉴数据下载”文件夹中
    targets = {2018: "N2019030122", 2017: "N2018050207", 2016:"N2017020368", 2015:"N2016120543", 2014:"N2016010176", 2013:"N2014050074", 2012:"N2013020020", 2011:"N2012040074"}
    for target in targets:
        year = target
        yearcode = targets[year]
        filedata(yearcode, year)

