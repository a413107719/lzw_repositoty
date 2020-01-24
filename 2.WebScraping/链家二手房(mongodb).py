#!/usr/bin/python 2.7
# -*- coding=UTF-8 -*-
import requests, re, time
from bs4 import BeautifulSoup
from retrying import retry
import random
import pymongo


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


def get_detailtext(link, pointname, pointprice, pointnum):
    global error_num, proxies_list, proxie_ip, special_num1, pageerrornum
    try:
        subweb_data = requests.get(link, proxies=proxie_ip)
        subsource = BeautifulSoup(subweb_data.text, 'lxml')
        imfor_list = []
        building_name = subsource.select("div.xiaoquDetailHeader > div > div.detailHeader.fl > h1")[0].string
        building_year = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(1) > span.xiaoquInfoContent')[0].string
        building_kind = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(2) > span.xiaoquInfoContent')[0].string
        building_fee = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(3) > span.xiaoquInfoContent')[0].string
        building_wygs = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(4) > span.xiaoquInfoContent')[0].string
        building_kfs = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(5) > span.xiaoquInfoContent')[0].string
        building_num = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(6) > span.xiaoquInfoContent')[0].string
        building_householdnum = subsource.select('div.xiaoquOverview > div.xiaoquDescribe.fr > div.xiaoquInfo > div:nth-child(7) > span.xiaoquInfoContent')[0].string

        building_xy = subsource.select('script:nth-child(' + str(23 + special_num1) + ')')
        text = str(building_xy[special_num1])
        regex = re.compile("(resblockPosition:')(\S+),(\S+)(')")
        mo = regex.search(text)
        building_x = mo.group(2)
        building_y = mo.group(3)


        pointimformation = [pointname, pointprice, pointnum, building_name, building_year, building_kind, building_fee,
                            building_wygs, building_kfs, building_num, building_householdnum, building_x, building_y]
        # 写入mongodb
        dict = {'名称': pointimformation[0], '单价': pointimformation[1], '在售套数': pointimformation[2],
                '别名': pointimformation[3], '建筑年代': pointimformation[4], '建筑类型': pointimformation[5],
                '物业费用': pointimformation[6], '物业公司': pointimformation[7], '开发商': pointimformation[8],
                '楼栋总数': pointimformation[9], '户数': pointimformation[10], '经度': pointimformation[11], '纬度': pointimformation[12]}
        mycolumn.update(dict, dict, True)
        print(pointimformation)

    except Exception as e:
        print('get_getailtext error: ', e, pointname, link)
        error_num += 1
        if error_num == 30:
            error_num = 0
            print("重新获取代理ip")
            proxies_list = get_10_proxies()
            change_proxies()
        if special_num1 == 1:
            special_num1 = 0
        elif special_num1 == 0:
            special_num1 = 1
        if pageerrornum == 4:
            print(pointname, '： 下载错误')
            return 0
        else:
            pageerrornum += 1
            change_proxies()
            get_detailtext(link, pointname, pointprice, pointnum)



# 获取主要信息
def get_pagetext(url):
    global proxie_ip, special_num1, pageerrornum
    special_num1 = 1
    web_data = requests.get(url, proxies=proxie_ip)
    source = BeautifulSoup(web_data.text,'lxml')

    names, links, prices, nums = [], [], [], []
    Loupannames = source.select('div.leftContent > ul > li > div.info > div.title > a')
    Loupanprices = source.select("div.leftContent > ul > li > div.xiaoquListItemRight > div.xiaoquListItemPrice > div.totalPrice > span")
    Loupannums = source.select("div.leftContent > ul > li > div.xiaoquListItemRight > div.xiaoquListItemSellCount > a > span")

    for i in range(len(Loupannames)):
        pageerrornum = 0
        pointlink = Loupannames[i]['href']
        pointname = Loupannames[i].string
        pointprice = Loupanprices[i].string
        pointnum = Loupannums[i].string

        names.append(pointname)
        links.append(pointlink)
        prices.append(pointprice)
        nums.append(pointnum)
        # print(pointname, pointprice, pointnum, pointlink, sep='  ')
        # mongodb查重
        findresult = mycolumn.find({'名称': pointname, '单价': pointprice})
        num = len(list(findresult))
        if num != 1:
            value = get_detailtext(pointlink, pointname, pointprice, pointnum)
            if value == 0:
                continue
        else:
            print(pointname, '： 已存在')


# get pagesURL
if __name__ == '__main__':
    mainurl = 'https://cd.lianjia.com/xiaoqu/xindou/'
    pagenum = 29

    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['zkStudio']
    mycolumn = mydb['lianjia_ershou']

    error_num = 0
    print("开始下载.....")
    proxies_list = get_10_proxies()
    change_proxies()
    for i in range(pagenum):
        url = mainurl +'pg%s'%str(i+1)
        get_pagetext(url)
        print("第%s页下载完毕"%str(i+1))
        time.sleep(1)  # 时间保护

    # get_detailtext1('https://cd.lianjia.com/xiaoqu/1611063956580/', 'name', 1000, 50)
