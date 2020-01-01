import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup
from retrying import retry
import random
import pymongo


# 从模板excel提取需要爬取的数据类
def get_kindscrapt():
    wb = openpyxl.load_workbook("D:\\tuba\\tubascriptlist.xlsx")
    sheetname = wb.sheetnames[0]
    sheet = wb[sheetname]
    maxrow = sheet.max_row
    maxcolumn = sheet.max_column

    list = []
    for y in range(1,maxcolumn+1):
        for i in range(2, maxrow + 1):
            cellvalue = sheet.cell(i, y).value
            if cellvalue is None:
                break
            else:
                list.append(cellvalue)
    return list


# 找到需要爬取的数据大类名称和链接
@retry(stop_max_attempt_number=3)
def kinds_data(mainurl):
    global proxies
    try:
        web_data = requests.get(mainurl, proxies=proxies)  # 找到目标页面所有分类名称和地址
        soup = BeautifulSoup(web_data.text, "html.parser")
        selects = soup.select('body > div.sort.cl > div > div > a')
        kind_names = []
        kind_urls = []
        for i in selects:
            kind_names.append(i.getText())
            kind_urls.append(i.get("href"))

        # 从模板excel提取需要爬取的数据类
        scraptlist = get_kindscrapt()
        kinds_willscrapt_name = []
        kinds_willscrapt_url = []
        for kind_name, kind_url in zip(kind_names, kind_urls):
            if kind_name in scraptlist:
                kinds_willscrapt_name.append(kind_name)
                kinds_willscrapt_url.append(kind_url)
        return kind_names, kind_urls

    except Exception as e:
        print(e, mainurl)
        print("kinds_data出错，重新请求")
        time.sleep(5)
        proxies = get_proxies()
        kinds_data(mainurl)


# 得到一个类所有点的链接
@retry(stop_max_attempt_number=3)
def kind_allpoints_data(kinds_url):
    global proxies
    try:
        web_data = requests.get(kinds_url, proxies=proxies)
        soup = BeautifulSoup(web_data.text, "html.parser")
        selects = soup.select('div.sort.cl > div.sortC > dl > dd > a')

        namelist, linklist = [], []
        for i in selects:
            namelist.append(i.getText())
            linklist.append(i.get("href"))
        return namelist, linklist
    except Exception as e:
        print(e, kinds_url)
        print("get_allpoints_namelink出错，重新请求")
        time.sleep(2)
        proxies = get_proxies()
        kind_allpoints_data(kinds_url)


# 找到所有点的信息
def get_pointimformation(namelist, linklist, kind_name):
    global kinds_all_list
    print('\n' + "重新验证代理是否成功：")
    print(proxies)
    kinds_all_list = []
    count = 0
    for name, pointurl in zip(namelist, linklist):
        findresult = mycolumn.find({"kind": kind_name, "name":name})
        num = len(list(findresult))
        if num != 1:
            point_data(name, pointurl, kind_name)  # 找到每个点的具体信息
        else:
            print(name + '：已经存在')

# 找到每个点的具体信息
@retry(stop_max_attempt_number=3)
def point_data(name, point_url, kind_name):
    global proxies
    try:
        web_data = requests.get(point_url, proxies=proxies)
        soup = BeautifulSoup(web_data.text, "html.parser")
        names = soup.find_all('meta')
        text = names[2].get('content')  # province=四川;city=自贡;coord=104.76247,29.37363
        textregex = re.compile(r'province=(\S\S);city=(\S\S);coord=(\d+\W\d+),(\d+\W\d+)')
        mo = textregex.search(text)
        if mo is not None:
            province, city, lattitude, longitude = mo.groups()
            kinds_all_list.append([name, kind_name, province, city, lattitude, longitude])
            print(str(len(kinds_all_list)) + ':' + str([name, kind_name, province, city, lattitude, longitude]))

            # 写入mongodb
            pointimformation = [name, kind_name, province, city, lattitude, longitude]                       
            dict = {'name': pointimformation[0], 'kind': pointimformation[1], 'province': pointimformation[2],
                    'city': pointimformation[3], 'longitude': pointimformation[4], 'latitude': pointimformation[5]}
            mycolumn.update(dict, dict, True)
            
        else:
            print("此链接没信息：" + point_url)

    except Exception as e:
        print(e, point_url)
        print("point_data出错，重新请求")
        time.sleep(5)
        proxies = get_proxies()
        point_data(name, point_url, kind_name)


# 获取代理IP，并合成一个proxise
def get_proxies():
    url = "http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4"  # 从代理网站上获取的url
    page = requests.get(url)
    ip = page.text
    proxy_ip = 'http://' + ip.split('\r')[0]
    proxies = {'http': proxy_ip}      # {'http': 'http://58.218.214.141:4549'}
    print("代理列表抓取成功: " + proxy_ip)
    return proxies


def main():
    global quelist, proxies
    quelist = []
    proxies = get_proxies()
    kindscraptname, kindscrapturl = kinds_data(main_url)  # 找到需要爬取的数据大类名称和链接
    for i in range(len(kindscraptname)):
        kindname = kindscraptname[i]
        kindurl = kindscrapturl[i]
        try:   # 找到每一个类的所有点的名称和链接
            kind_allpoints_name, kind_allpoints_url = kind_allpoints_data(kindurl)
            print(kind_allpoints_name, kind_allpoints_url)

            # 判断此类数据在mongodb中的数量是否一致，如果一致则跳过分类
            kind_number = len(kind_allpoints_name)
            findresult = mycolumn.find({"kind": kindname})
            print(kind_number,len(list(findresult)))
            if kind_number == len(list(findresult)):
                continue
            get_pointimformation(kind_allpoints_name, kind_allpoints_url, kindname)

        except Exception as e:
            print(e)
            main()


if __name__ == '__main__':
    main_url = 'http://poi.mapbar.com/chengdu/'
    output_path = 'D:\\tuba\\'
    excelpath = output_path + 'tuban.xlsx'
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['zkStudio']
    mycolumn = mydb['tuba']
    main()
