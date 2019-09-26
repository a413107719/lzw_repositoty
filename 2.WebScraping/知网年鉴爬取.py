#!/usr/bin/env python
# coding:utf-8
from selenium import webdriver
import urllib.request
from bs4 import BeautifulSoup
import requests
import time
import random
import re
import os
from retrying import retry


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


# 让函数报错后继续重新执行，达到最大执行次数的上限后才判断链接失效，不再继续执行。
@retry(stop_max_attempt_number=3)
def filedown(title, url, year):  # 文件下载函数
    try:
        print(title, url, year, sep=" ")

        # 创建文件夹
        folder = "D:\\YearbookDownload"
        path = folder + '\\' + str(year) + '\\'
        if os.path.isdir(path):
            # print("已有路径：" + path)
            pass
        else:
            os.makedirs(path)
            # print("成功创建：" + path)

        # 排除已经存在的表格
        if "—" in title:
            title = title.replace("—", "-")
        if os.path.exists(path + title+".xls"):
            print("已经存在表格：" + title)
        else:
            # 设置Firefox参数
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.dir', path)  # 现在文件存放的目录
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
            # 下载excel
            browser = webdriver.Firefox(firefox_profile=profile)
            browser.get(url)
            x = browser.find_element_by_id("Button2")
            x.click()
            sleeptime = random.randint(2, 3)
            time.sleep(sleeptime)
            # 重命名
            codename = url.split("=")[1]
            files = os.listdir(path)
            for file in files:
                if "-" in file or "_" not in file:
                    continue
                x = file.split("N")[1].split(".")[0]
                y = codename.split("N")[1]
                if x == y:
                    os.rename(path + file, path + title + ".xls")
                    print("匹配到数据：" + title + '正在重命名。。。')
                else:
                    print("未匹配数据，应该不会发生")
            browser.quit()

    except Exception as e:
        print("error")
        pass


if __name__ == '__main__':
    # 默认下载到D盘的“年鉴数据下载”文件夹中
    # 'GuangXi2018': "N2018110018", 'GuangXi2017': "N2017120295", 'GuangXi2016': "N2017020374", 'GuangXi2015': "N2016010072", 'GuangXi2014': "N2014120093", 'GuangXi2013': "N2013110048",
    # 'GuiLin2018': "N2019030108", 'GuiLin2017': "N2018050237", 'GuiLin2015': "N2016120526", 'GuiLin2016': "N2017060049", 'GuiLin2014': "N2015040003", 'GuiLin2013': "N2014050092",
    targets = {
        'GuiZou2018': "N2019010158", 'GuiZou2017': "N2017120264", 'GuiZou2015': "N2016010122", 'GuiZou2016': "N2017020211", 'GuiZou2014': "N2014120128", 'GuiZou2013': "N2013120102",
        'HuNan2018': "N2019040070", 'HuNan2017': "N2018050230", 'HuNan2015': "N2016010070", 'HuNan2016': "N2017020284", 'HuNan2014': "N2014120095", 'HuNan2013': "N2013120093"
    }
    for target in targets:
        print("开始爬取 %s 的数据"%target)
        year = target
        yearcode = targets[year]
        filedata(yearcode, year)
        print("已经完成 " + str(year) + " 年数据的爬取")
        time.sleep(5)

