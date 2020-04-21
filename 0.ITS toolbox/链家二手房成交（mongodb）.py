# -*- coding=UTF-8 -*-
import requests, re, time
from bs4 import BeautifulSoup
from retrying import retry
import random
import pymongo


def get_10_proxies():
    try:

        url = "http://http.tiqu.alicdns.com/getip3?num=10&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4"  # 从代理网站上获取的url
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


def get_pagenum(link):
    global proxies_list, proxie_ip
    try:
        subweb_data = requests.get(link, proxies=proxie_ip)
        subsource = BeautifulSoup(subweb_data.text, 'lxml')
        text = subsource.select("div.content > div.leftContent > div.contentBottom.clear > div.page-box.fr > div")[0]
        regex = re.compile('("totalPage":)(\d+),')
        mo = regex.search(str(text))
        if mo is None:
            raise Exception
        else:
            pagenum = int(mo.group(2))
            print("页数：", pagenum)
            return pagenum
    except Exception as e:
        print('get_pagenum error: ', e, link)
        change_proxies()
        get_pagenum(link)


def get_singlepage_namesandlinks(link):
    global proxies_list, proxie_ip
    try:
        name_list = []
        url_list = []
        subweb_data = requests.get(link, proxies=proxie_ip)
        subsource = BeautifulSoup(subweb_data.text, 'lxml')
        textlist = subsource.select("div.content > div.leftContent > ul > li > div > div.title > a")
        for text in textlist:
            name = text.string
            url = text['href']
            # print(name,url)
            name_list.append(name)
            url_list.append(url)
        return name_list, url_list
    except Exception as e:
        print('get_singlepage_namesandlinks error: ', e, link)
        change_proxies()
        get_singlepage_namesandlinks(link)


def get_xy(sub_source, num):
    global proxies_list, proxie_ip
    try:
        text = "script:nth-child(" + str(num) + ")"
        building_xy = sub_source.select(text)
        text = str(building_xy)
        regex = re.compile("(resblockPosition:')(\S+),(\S+)(')")
        mo = regex.search(text)
        if mo is None:
            raise Exception
        else:
            building_x = mo.group(2)
            building_y = mo.group(3)
            # print(building_x, building_y)
            return building_x, building_y
    except Exception as e:
        print("get_xy error", e)
        get_xy(sub_source, 24)



def get_detalimformation(name, link):
    global proxies_list, proxie_ip
    try:
        subweb_data = requests.get(link, proxies=proxie_ip)
        subsource = BeautifulSoup(subweb_data.text, 'lxml')
        dealprice = subsource.select("section.wrapper > div.overview > div.info.fr > div.price > span > i")[0].string
        averageprice = subsource.select("section.wrapper > div.overview > div.info.fr > div.price > b")[0].string
        onsaleprice = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(1) > label")[0].string
        totaldays = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(2) > label")[0].string
        pricechangetimes = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(3) > label")[0].string
        bringtohouse = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(4) > label")[0].string
        focals = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(5) > label")[0].string
        browse = subsource.select("section.wrapper > div.overview > div.info.fr > div.msg > span:nth-child(6) > label")[0].string

        housekind = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(1)")[0].stripped_strings)[1]
        totalarea = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(3)")[0].stripped_strings)[1]
        innerarea = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(5)")[0].stripped_strings)[1]
        facedirection = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(7)")[0].stripped_strings)[1]
        decoration = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(9)")[0].stripped_strings)[1]
        Property_rights = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(13)")[0].stripped_strings)[1]

        floor = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(2)")[0].stripped_strings)[1]
        housetype = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(4)")[0].stripped_strings)[1]
        buildingtype = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(6)")[0].stripped_strings)[1]
        builtyear = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(8)")[0].stripped_strings)[1]
        buildingstructure = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(10)")[0].stripped_strings)[1]
        ladder = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(12)")[0].stripped_strings)[1]
        elevator = list(subsource.select("div.introContent > div.base > div.content > ul > li:nth-child(14)")[0].stripped_strings)[1]

        lianjia_code = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(1)")[0].stripped_strings)[1]
        guapai_time = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(3)")[0].stripped_strings)[1]
        fangwu_year = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(5)")[0].stripped_strings)[1]
        jiaoyiquanshu = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(2)")[0].stripped_strings)[1]
        fangwuyongtu = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(4)")[0].stripped_strings)[1]
        fangquansuoshu = list(subsource.select("div.introContent > div.transaction > div.content > ul > li:nth-child(6)")[0].stripped_strings)[1]



        # 写入mongodb
        dict = {'名称': name, '成交总价': dealprice, '楼面价': averageprice, '挂牌价格': onsaleprice,
                '成交周期': totaldays, '调价次数': pricechangetimes, '带看次数': bringtohouse,
                '关注人数': focals, '浏览次数': browse, '房屋户型': housekind,
                '建筑面积': totalarea, '套内面积': innerarea, '房屋朝向': facedirection, '装修情况': decoration,
                '产权年限': Property_rights, '所在楼层': floor, '户型结构': housetype, '建筑类型': buildingtype,
                '建成年代': builtyear, '建筑结构': buildingstructure, '梯户比例': ladder, '配备电梯': elevator,
                '链家编号': lianjia_code, '挂牌时间': guapai_time, '房屋年限': fangwu_year, '交易权属': jiaoyiquanshu,
                '房屋用途': fangwuyongtu, '房权所属': fangquansuoshu, '链接': link
                }
        print(dict)
        print()
        mycolumn.update(dict, dict, True)

    except Exception as e:
        print('get_detalimformation error: ', e, name, link)
        change_proxies()
        get_detalimformation(name, link)


# get pagesURL
if __name__ == '__main__':
    mainurl = 'https://cd.lianjia.com/chengjiao/xindou/'

    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['zkStudio']
    mycolumn = mydb['lianjia_ershou_chengjiao']

    error_num = 0
    print("开始下载.....")
    proxies_list = get_10_proxies()
    change_proxies()

    for i in range(4, 9):   # 一共有9个面积分类
        suburl = mainurl + 'a' + str(i)
        print('\n', suburl)
        pagenum = get_pagenum(suburl)  # 获取页数
        for y in range(1, pagenum + 1):
            time.sleep(5)
            # 构造页网址
            pageurl = mainurl + 'pg' + str(y) + 'a' + str(i)
            print("第", y, "页：", pageurl)
            # 获取每一页的房源名称和链接
            namelist, urllist = get_singlepage_namesandlinks(pageurl)
            for fang_name,fang_url in zip(namelist, urllist):

                # print('mongo查重',fang_name,fang_url)
                # mongodb查重
                findresult = mycolumn.find({'名称': fang_name, '链接': fang_url})
                num = len(list(findresult))
                if num != 1:
                    get_detalimformation(fang_name, fang_url)   # 爬取详细信息
                else:
                    print(fang_name, '： 已存在')



