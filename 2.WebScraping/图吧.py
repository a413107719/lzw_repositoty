import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup
from retrying import retry
import random


# 从模板excel提取需要爬取的数据类
def get_kindscrapt():
    wb = openpyxl.load_workbook("D:\\tuba\\tubascriptlist.xlsx")
    sheetname = wb.sheetnames[0]
    sheet = wb.get_sheet_by_name(sheetname)
    maxrow = sheet.max_row
    list = []
    for i in range(1, maxrow + 1):
        cellvalue = sheet.cell(i, 2).value
        if cellvalue == '':
            break
        else:
            list.append(cellvalue)
    return list


# 找到需要爬取的数据大类名称和链接
@retry(stop_max_attempt_number=3)
def kinds_data(mainurl):
    global proxies
    try:
        # 找到目标页面所有分类名称和地址
        web_data = requests.get(mainurl, proxies=proxies)
        soup = BeautifulSoup(web_data.text, 'lxml')
        selects = soup.select('body > div.sort.cl > div > div > a')
        kind_names = []
        kind_urls = []
        for i in selects:
            kind_names.append(i.getText())
            kind_urls.append(i.get("href"))

        # 从模板excel提取需要爬取的数据类
        scraptlist = get_kindscrapt()
        # print(scraptlist)

        kinds_exist = []
        kinds_willscrapt_name = []
        kinds_willscrapt_url = []
        for kind_name, kind_url in zip(kind_names, kind_urls):
            if kind_name in scraptlist:
                # 先判断excel里是否有这类数据，如果存在则跳过
                create_excel()
                wb = openpyxl.load_workbook(excelpath)
                if kind_name in wb.get_sheet_names():  # 已经存在
                    kinds_exist.append(kind_name)
                else:
                    kinds_willscrapt_name.append(kind_name)
                    kinds_willscrapt_url.append(kind_url)
        print('已经存在：' + str(kinds_exist))
        print('需要爬取：' + str(kinds_willscrapt_name))
        return kinds_willscrapt_name, kinds_willscrapt_url

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
        soup = BeautifulSoup(web_data.text, 'lxml')
        selects = soup.select('div.sort.cl > div.sortC > dl > dd > a')
        # print(selects)

        namelist, linklist = [], []
        for i in selects:
            namelist.append(i.getText())
            linklist.append(i.get("href"))
        return namelist, linklist
    except Exception as e:
        print(e, kinds_url)
        print("get_allpoints_namelink出错，重新请求")
        time.sleep(5)
        proxies = get_proxies()
        time.sleep(3)
        kind_allpoints_data(kinds_url)


# 找到所有点的信息
def get_pointimformation(namelist, linklist, kind_name):
    global kinds_all_list
    print('\n' + "重新验证代理是否成功：")
    print(proxies)
    kinds_all_list = []
    count = 0
    for name, pointurl in zip(namelist, linklist):
        point_data(name, pointurl, kind_name)

        count += 1
        if count == 10:
            sleeptime = random.randint(2, 5)
            print("每爬取10个信息随机暂停：" + str(sleeptime) + '\n')
            time.sleep(sleeptime)
            count = 0
    return kinds_all_list


# 找到每个点的具体信息
@retry(stop_max_attempt_number=3)
def point_data(name, point_url, kind_name):
    global proxies
    try:
        web_data = requests.get(point_url, proxies=proxies)
        soup = BeautifulSoup(web_data.text, 'lxml')
        names = soup.find_all('meta')
        text = names[2].get('content')  # province=四川;city=自贡;coord=104.76247,29.37363
        textregex = re.compile(r'province=(\S\S);city=(\S\S);coord=(\d+\W\d+),(\d+\W\d+)')
        mo = textregex.search(text)
        if mo is not None:
            province, city, lattitude, longitude = mo.groups()
            kinds_all_list.append([name, kind_name, province, city, lattitude, longitude])
            print(str(len(kinds_all_list)) + ':' + str([name, kind_name, province, city, lattitude, longitude]))
        else:
            print("此链接没信息：" + point_url)

    except Exception as e:
        print(e, point_url)
        print("point_data出错，重新请求")
        time.sleep(5)
        proxies = get_proxies()
        point_data(point_url)


# 创建excel
def create_excel():
    if not os.path.exists(output_path):
        print("正在创建文件夹：" + output_path)
        os.makedirs(output_path)
        wb = openpyxl.Workbook()
        wb.save(excelpath)
    elif not os.path.exists(excelpath):
        print("存在文件夹，但无excel")
        wb = openpyxl.Workbook()
        wb.save(excelpath)
    else:
        pass
        # print('已存在excel文件')


# 写入Excel
def write2excel(kindname, allpoints_information):
    wb = openpyxl.load_workbook(excelpath)
    wb.create_sheet(kindname)
    sheet = wb[kindname]  # 选择一个excel页面
    # 表格填入数据
    sheet.cell(row=1, column=1).value = "名称"
    sheet.cell(row=1, column=2).value = "类型"
    sheet.cell(row=1, column=3).value = "省名"
    sheet.cell(row=1, column=4).value = "市名"
    sheet.cell(row=1, column=5).value = "经度"
    sheet.cell(row=1, column=6).value = "纬度"

    for row in range(2, len(allpoints_information) + 2):
        sheet.cell(row=row, column=1).value = allpoints_information[row - 2][0]
        sheet.cell(row=row, column=2).value = allpoints_information[row - 2][1]
        sheet.cell(row=row, column=3).value = allpoints_information[row - 2][2]
        sheet.cell(row=row, column=4).value = allpoints_information[row - 2][3]
        sheet.cell(row=row, column=5).value = allpoints_information[row - 2][4]
        sheet.cell(row=row, column=6).value = allpoints_information[row - 2][5]
    wb.save(excelpath)
    print('已经下载数据')


# 获取代理IP，并合成一个proxise
def get_proxies():
    url = "http://http.tiqu.alicdns.com/getip3?num=1&type=3&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=2&sb=0&pb=4&mr=1&regions="  # 从代理网站上获取的url
    page = requests.get(url)
    iplist = page.text
    ip_list = iplist.split('</br>')
    # print(len(ip_list)-1)
    if len(ip_list) == 1:
        print("代理列表抓取失败！")
    print("代理列表抓取成功: " + str(iplist))
    ip = ip_list[:-1][0]

    proxy_ip = 'http://' + ip
    proxies = {'http': proxy_ip}
    print(proxies)
    return proxies


def main():
    global quelist, proxies
    quelist = []
    proxies = get_proxies()
    kindscraptname, kindscrapturl = kinds_data(main_url)  # 找到需要爬取的数据大类名称和链接
    for i in range(len(kindscraptname)):
        kindname = kindscraptname[i]
        kindurl = kindscrapturl[i]
        # 找到每一个类的所有点的名称和链接
        try:
            kind_allpoints_name, kind_allpoints_url = kind_allpoints_data(kindurl)
        except Exception as e:
            print(e)
            main()
        kind_allpoints_information = get_pointimformation(kind_allpoints_name, kind_allpoints_url, kindname)
        # 写入excel
        write2excel(kindname, kind_allpoints_information)


if __name__ == '__main__':
    main_url = 'http://poi.mapbar.com/liuzhou/'
    output_path = 'D:\\tuba\\'
    excelpath = output_path + 'tuban.xlsx'
    main()
