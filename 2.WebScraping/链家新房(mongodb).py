#!/usr/bin/python 2.7
# -*- coding=UTF-8 -*-
# 能爬取数据，但未写入文件或数据库
from bs4 import BeautifulSoup
import requests
import re
import time
import pymongo
import random


def get_10_proxies():
    try:
        url = "http://webapi.http.zhimacangku.com/getip?num=10&type=1&pro=&city=0&yys=0&port=1&pack=79679&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="  # 从代理网站上获取的url
        page = requests.get(url)
        ip = page.text
        if ip == '{"code": 115, "data": [], "msg": "请重新提取", "success": false}':
            raise Exception('"code": 115, "data": [], "msg": "请重新提取"')
        elif ip == 'http://{"code":111,"data":[],"msg":"请2秒后再试","success":false}':
            raise Exception('"code":111,"data":[],"msg":"请2秒后再试"')
        else:
            iplist = ip.split("\r\n")
            iplist.pop()
        proxies =[]
        for i in iplist:
            proxie = 'http://' + i
            proxies.append(proxie)
        print("代理列表：", proxies)
        if proxies == []:
            raise Exception("代理为空，重新获取！")
        return proxies
    except Exception as e:
        print("未能获取有效代理地址:")
        print(e)
        time.sleep(5)
        get_10_proxies()


# 切换代理
def change_proxies():
    global proxies_list, proxie_ip
    ip = random.sample(proxies_list,1)[0]
    proxie_ip = {'https': ip}   # 写成https就能爬取了，不知道tmd什么原因
    print(proxie_ip)


def get_pagetext(url):
    global proxie_ip, special_num1, pageerrornum
    special_num1 = 14
    web_data = requests.get(url, proxies=proxie_ip)
    source = BeautifulSoup(web_data.text,'lxml')
    names, prices, areas, address, urls = [], [], [], [], []
    Loupannames = source.select('body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-name > a')
    Loupanprices = source.select('body > div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-price > div.main-price > span.number')
    Loupanareas = source.select("div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-area > span")
    Loupanaddress = source.select("div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-location > a")
    Lopanurl = source.select("div.resblock-list-container.clearfix > ul.resblock-list-wrapper > li > div > div.resblock-name > a")
    for i in range(len(Loupannames)):
        pageerrornum = 0
        pointname = Loupannames[i].string
        pointprice = Loupanprices[i].string
        pointarea = Loupanareas[i].string
        pointaddress = Loupanaddress[i].string
        pointurl = 'https://cd.fang.lianjia.com' + Lopanurl[i]['href']
        pointxiangqingurl = pointurl + 'xiangqing/'

        # mongodb查重
        findresult = mycolumn.find({'名称': pointname, '均价': pointprice})
        num = len(list(findresult))
        if num != 1:
            get_detailtext(pointurl, pointxiangqingurl, pointname, pointprice, pointarea, pointaddress)
        else:
            print(pointname, '： 已存在')


def data_standarize(list):
    newlist = []
    invalid_characaters = "、()（）:：，。!@#$^&*_<=,+[]{}\\;,',.?/\n)＃'%％±\xa0"
    for strings in list:
        for c in invalid_characaters:
            strings = strings.replace(c, "")
        strings = strings.replace(" ", "")
        strings = strings.replace("　", "")
        newlist.append(strings)
    # print("已完成特殊字符清洗")
    return newlist


def get_detailtext(point_url, point_xiangqingurl, point_name, point_price, point_area, point_address):
    global error_num, proxies_list, proxie_ip, special_num1, pageerrornum
    try:
        subweb_data = requests.get(point_xiangqingurl, proxies=proxie_ip)
        subsource = BeautifulSoup(subweb_data.text, 'lxml')
        point_kind = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(2) > li:nth-child(1) > span.label-val")[0].string
        point_averageprice = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(2) > li:nth-child(2) > span.label-val > span")[0].string
        point_keyword = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(2) > li:nth-child(3) > span.label-val.tese-val")[0].string
        point_kfs = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(2) > li:nth-child(7) > span.label-val")[0].string
        point_jzlx = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(8) > li:nth-child(1) > span.label-val")[0].string
        point_zdmj = data_standarize([subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(8) > li:nth-child(3) > span.label-val")[0].string])[0]
        point_jzmj = data_standarize([subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(8) > li:nth-child(5) > span.label-val")[0].string])[0]
        point_ghhs = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(8) > li:nth-child(7) > span.label-val")[0].string
        point_cqnx = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(8) > li:nth-child(8) > span.label-val")[0].string

        point_wygs = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(" + str(special_num1) + ") > li:nth-child(1) > span.label-val")[0].string
        point_wyfee = subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(" + str(special_num1) + ") > li:nth-child(3) > span.label-val")[0].string
        point_cws = data_standarize([subsource.select("div.add-panel.clear > div.big-left.fl > ul:nth-child(" + str(special_num1) + ") > li:nth-child(7) > span.label-val")[0].string])[0]
        print(point_name, ': 基础信息爬取完成')

        subweb_data1 = requests.get(point_url, proxies=proxie_ip)
        subsource1 = BeautifulSoup(subweb_data1.text, 'lxml')
        point_xy = subsource1.select("div.mod-global > div.mod-wrap.mod-banner > div.album > #mapWrapper")

        point_kpsj = subsource1.select("div.mod-global > div.mod-wrap.mod-banner > div.resblock-info.animation.qr-fixed > div > div.middle-info.animation > ul > li.info-item.open-date-wrap > div > span.content")[0].string
        text = str(point_xy[0])
        regex = re.compile('(data-coord=")(\S+),(\S+)(")')
        mo = regex.search(text)
        point_x = mo.group(2)
        point_y = mo.group(3)
        print(point_name, ': 坐标爬取完成')

        pointimformation = [point_name, point_price, point_area, point_address, point_kind, point_keyword, point_kfs,
                            point_jzlx, point_zdmj, point_jzmj, point_ghhs, point_cqnx,point_wygs, point_wyfee,
                            point_cws, point_x, point_y, point_kpsj]
        # 写入mongodb
        dict = {'名称': pointimformation[0], '均价': pointimformation[1], '建面': pointimformation[2],
                '地址': pointimformation[3], '物业类型': pointimformation[4], '项目特色': pointimformation[5],
                '开发商': pointimformation[6], '建筑类型': pointimformation[7], '占地面积': pointimformation[8],
                '建筑面积': pointimformation[9], '规划户数': pointimformation[10], '产权年限': pointimformation[11],
                '物业公司': pointimformation[12], '物业费用': pointimformation[13], '车位数': pointimformation[14],
                '经度': pointimformation[15], '纬度': pointimformation[16], '开盘时间': pointimformation[17]}
        mycolumn.update(dict, dict, True)
        print(pointimformation)
        print()

    except Exception as e:
        print('get_getailtext error: ', e, point_name, point_url)
        error_num += 1
        if error_num == 30:
            error_num = 0
            print("重新获取代理ip")
            proxies_list = get_10_proxies()
            change_proxies()
        if special_num1 == 13:
            special_num1 = 14
        elif special_num1 == 14:
            special_num1 = 13

        if pageerrornum == 4:
            print(point_name, '： 下载错误')
            return 0
        else:
            pageerrornum += 1
            change_proxies()
            get_detailtext(point_url, point_xiangqingurl, point_name, point_price, point_area, point_address)


# get pagesURL
if __name__ == '__main__':
    mainurl = 'https://cd.fang.lianjia.com/loupan/xindou/'
    pagenum = 29

    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['zkStudio']
    mycolumn = mydb['lianjia_xinfang']

    error_num = 0
    print("开始下载.....")
    proxies_list = get_10_proxies()
    change_proxies()
    for i in range(pagenum):
        url = mainurl + 'pg%s' % str(i + 1)
        get_pagetext(url)
        print("第%s页下载完毕" % str(i + 1))
        time.sleep(1)  # 时间保护


