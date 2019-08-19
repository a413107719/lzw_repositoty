import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup
from retrying import retry
import random


# 找到各类型链接
def kinds_data(point_url):
    web_data = requests.get(point_url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    selects = soup.select('body > div.sort.cl > div > div > a')
    print(selects)
    kind_names = []
    kind_urls = []
    for i in selects:
        kind_names.append(i.getText())
        kind_urls.append(i.get("href"))
    for kind_name, kind_url in zip(kind_names, kind_urls):
        print('\n', '<<', kind_name, kind_url, '>>')
        # 先判断excel里是否有这类数据，如果存在则跳过
        create_excel()
        wb = openpyxl.load_workbook(excelpath)
        if kind_name in wb.get_sheet_names():
            print("已经存在此类数据,将爬取下一个分类")
        else:
            features_imformation = pack_imformation(kind_url, kind_name)  # 得到一个类所有点的信息
            # 写入Excel
            write2excel(kind_name, features_imformation)


# 得到一个类所有点的信息
@retry(stop_max_attempt_number=3)
def pack_imformation(kinds_url, kinds_name):
    kinds_all_list = []
    web_data = requests.get(kinds_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    selects = soup.select('div.sort.cl > div.sortC > dl > dd > a')
    # print(selects)

    namelist, linklist = [], []
    for i in selects:
        namelist.append(i.getText())
        linklist.append(i.get("href"))
    count = 0
    for name, pointlink in zip(namelist, linklist):
        # print( name, pointlink)
        try:
            if point_data(pointlink) is None:
                print("将不填入信息")
            else:
                province, city, lattitude, longitude = point_data(pointlink)
                print(name, kinds_name, province, city, lattitude, longitude, pointlink)
                kinds_all_list.append([name, kinds_name, province, city, lattitude, longitude])
        except Exception as e:
            print(e, pointlink)
            print("出错，重新请求")
            time.sleep(10)
            pack_imformation(kinds_url, kinds_name)

        count += 1
        if count == 10:
            sleeptime = random.randint(5, 10)
            print("每爬取10个信息随机暂停：" + str(sleeptime) + '\n')
            time.sleep(sleeptime)
            count = 0
    return kinds_all_list


# 找到每个点的信息
@retry(stop_max_attempt_number=3)
def point_data(point_url):
    try:
        web_data = requests.get(point_url)
        soup = BeautifulSoup(web_data.text,'lxml')
        names = soup.find_all('meta')
        text = names[2].get('content')       #province=四川;city=自贡;coord=104.76247,29.37363
        textregex = re.compile(r'province=(\S\S);city=(\S\S);coord=(\d+\W\d+),(\d+\W\d+)')
        mo = textregex.search(text)
        if mo is not None:
            province, city, lattitude, longitude = mo.groups()
            return province, city, lattitude, longitude
        else:
            print("此链接没信息：" + point_url)
            return None

    except Exception as e:
        print(e, point_url)
        print("出错，重新请求")
        time.sleep(10)
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
        print('已存在excel文件')


# 写入Excel
def write2excel(kindname, featuresimformation):
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

    for row in range(2, len(featuresimformation)+2):
        sheet.cell(row=row, column=1).value = featuresimformation[row-2][0]
        sheet.cell(row=row, column=2).value = featuresimformation[row-2][1]
        sheet.cell(row=row, column=3).value = featuresimformation[row-2][2]
        sheet.cell(row=row, column=4).value = featuresimformation[row-2][3]
        sheet.cell(row=row, column=5).value = featuresimformation[row-2][4]
        sheet.cell(row=row, column=6).value = featuresimformation[row-2][5]
    wb.save(excelpath)
    print('已经下载数据')


main_url = 'http://poi.mapbar.com/liuzhou/'
output_path = 'D:\\tuba\\'
excelpath = output_path + 'tuban.xlsx'
kinds_data(main_url)

