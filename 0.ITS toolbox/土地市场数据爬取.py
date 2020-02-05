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
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import requests
import re
import time
import pymongo
import random


def get_page_projects(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Cookie": "ASP.NET_SessionId=r0vsly55ie3cv2454f120c55; global_cookie=bxhworgu2qr5aajj35myzl6mo20k69a8kpn; Hm_lvt_e60c55838acbc89c7409eced091b4723=1580905369; Hm_lvt_53d94eb4421c8445dba94dfb21a76732=1580905372; userguid=Zev5Sbd67qApDlVRwZoq1gj2E2kGSd1qZ7euB0fHQdkPlD8f3cIs9A==; uservisitMarketitem=02fb524f-5460-425b-8cb9-7ddd0bd7e217%257c%257c2020%252f2%252f5%2b20%253a47%253a24; Hm_lpvt_e60c55838acbc89c7409eced091b4723=1580907602; Hm_lpvt_53d94eb4421c8445dba94dfb21a76732=1580907602; unique_cookie=U_bxhworgu2qr5aajj35myzl6mo20k69a8kpn*15",
        "Host": "land.3fang.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    web_data = requests.get(url,headers=headers)
    source = BeautifulSoup(web_data.text,'html5lib')    # beautifulsoup解析html后内容缺失，使用'html5lib'替代'lxml'解决问题
    namelinks = source.select("div.list28_text.fl > h3 > a")
    areas = source.select("#landlb_B04_22 > dd > div.list28_text.fl > table > tbody > tr:nth-child(2) > td:nth-child(2)")

    for i in range(len(namelinks)):
        project_name = namelinks[i].get("title")
        project_url = "https://land.3fang.com" + namelinks[i].get("href")
        project_area = areas[i].getText()
        print('[', project_name, project_area, project_url, ']')

        # mongodb查重
        findresult = mycolumn.find({"URL": project_url})
        num = len(list(findresult))
        if num != 1:
            get_detail_imformation(project_url)
        else:
            print(project_name, '： 已存在')
        print()


def get_detail_imformation(url):
    # print(url)
    web_data = requests.get(url)
    source = BeautifulSoup(web_data.text, 'html5lib')  # beautifulsoup解析html后内容缺失，使用'html5lib'替代'lxml'解决问题
    name = source.select("#printData1 > div.tit_box01")[0].getText()
    land_num = str(source.select("#printData1 > div.menubox01.mt20 > span")[0].getText()).split('：')[1]
    # print(name, land_num, sep='\n')

    province = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(1) > td:nth-child(1) > a")[0].getText()
    area = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(2) > td:nth-child(1) > em")[0].getText()
    building_area = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(3) > td:nth-child(1) > em")[0].getText()
    floorarea_ratio = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(4) > td:nth-child(1)")[0].getText()).split('：')[1]
    commercial_ratial = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(5) > td:nth-child(1)")[0].getText()).split('：')[1]
    height = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(1)")[0].getText()).split('：')[1]
    land_year = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(1)")[0].getText()).split('：')[1]
    sizhi = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(8) > td:nth-child(1)")[0].getText()).split('：')[1]
    # print(province, area, building_area, floorarea_ratio, commercial_ratial, height, land_year, sizhi, sep='\n')
    # print()

    city = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(1) > td:nth-child(2) > a")[0].getText()
    land_area = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(2) > td:nth-child(2) > em")[0].getText()
    daizheng_area = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(3) > td:nth-child(2) > em")[0].getText()
    green_ratio = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(4) > td:nth-child(2)")[0].getText()).split('：')[1]
    building_density = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(5) > td:nth-child(2)")[0].getText()).split('：')[1]
    churangxingshi = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(6) > td:nth-child(2)")[0].getText()).split('：')[1]
    location = str(source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(7) > td:nth-child(2)")[0].getText()).split('：')[1]
    usage = source.select("#printData1 > div:nth-child(5) > table > tbody > tr:nth-child(8) > td:nth-child(2) > a")[0].getText()
    # print(city, land_area, daizheng_area, green_ratio, building_density, churangxingshi, location, usage, sep='\n')
    # print()

    jiaoyizhuangkuang = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(1)")[0].getText()).split('：')[1]
    begin_time = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(2) > td:nth-child(1)")[0].getText()).split('：')[1]
    deal_time = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(3) > td:nth-child(1)")[0].getText()).split('：')[1]
    begin_price = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(1)")[0].getText()).split('：')[1]
    floorland_price = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(5) > td:nth-child(1)")[0].getText()).split('：')[1]
    security_price = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(7) > td:nth-child(1)")[0].getText()).split('：')[1]
    # print(jiaoyizhuangkuang, begin_time, deal_time, begin_price, floorland_price, security_price, sep='\n')
    # print()

    price_owner = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(1) > td:nth-child(2)")[0].getText()).split('：')[1]
    end_time = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(2) > td:nth-child(2)")[0].getText()).split('：')[1]
    exchange_location = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(3) > td:nth-child(2)")[0].getText()).split('：')[1]
    get_price = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(4) > td:nth-child(2)")[0].getText()).split('：')[1]
    addprice_ratio = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(5) > td:nth-child(2)")[0].getText()).split('：')[1]
    miniadd_price = str(source.select("#printData1 > div:nth-child(5) > div.banbox > table > tbody > tr:nth-child(7) > td:nth-child(2)")[0].getText()).split('：')[1]
    # print(price_owner, end_time, exchange_location, get_price, addprice_ratio, miniadd_price, sep='\n')
    # print()

    if jiaoyizhuangkuang != "未成交":
        location2 = source.select("#wrapper > div.clearfix > div.w300.fr > div:nth-child(2) > iframe")[0].get("src")
        x = str(location2).split("pointx=")[1].split("&pointy=")[0]
        y = str(location2).split("pointx=")[1].split("&pointy=")[1]
    else:
        x = 0
        y = 0
    # print(x, y)

    # 写入mongodb
    dict = {
        "土地名称": name, "地块编号": land_num, "URL": url,
        "地区": province, "总面积": area, "规划建筑面积": building_area, "容积率": floorarea_ratio, "商业比例": commercial_ratial, "限制高度": height, "出让年限": land_year, "四至": sizhi,
        "所在地": city, "建设用地面积": land_area, "代征面积": daizheng_area, "绿化率": green_ratio, "建筑密度": building_density, "出让形式": churangxingshi, "位置": location, "规划用途": usage,
        "交易状况": jiaoyizhuangkuang, "起始日期": begin_time, "成交日期": deal_time, "起始价": begin_price, "楼面价": floorland_price, "保证金": security_price,
        "竞得方": price_owner, "截止日期": end_time, "交易地点": exchange_location, "成交价": get_price, "溢价率": addprice_ratio, "最小加价幅度": miniadd_price,
        "经度": x, "纬度": y
    }
    print(dict)
    mycolumn.update(dict, dict, True)


if __name__ == '__main__':
    mainurl = 'https://land.3fang.com/market/510100_510114_______1_0_1.html'
    pagenum = 20

    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['zkStudio']
    mycolumn = mydb['tudi_zhaopaigua']

    print("开始下载.....")
    url_regex = re.compile(r"\d.html")
    match = url_regex.search(mainurl).group()
    mainurl_begin = mainurl.split(match)[0]
    for i in range(pagenum):
        url = mainurl_begin + str(i + 1) + '.html'
        # print(url)
        get_page_projects(mainurl)  # 找到每页所有项目
        print("第%s页下载完毕" % str(i + 1))
        time.sleep(1)  # 时间保护
        # break


