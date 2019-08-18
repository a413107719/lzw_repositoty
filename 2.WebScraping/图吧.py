import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup
from retrying import retry


# 找到各类型链接
def kinds_data(point_url):
    web_data = requests.get(point_url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    selects = soup.select('body > div.sort.cl > div > div > a')
    print(selects)
    titles = []
    kinds_urls = []
    for i in selects:
        titles.append(i.getText())
        kinds_urls.append(i.get("href"))
    print(titles)
    print(kinds_urls)

    for title, url in zip(titles, kinds_urls):
        print(title, url)
        pack_imformation(url, title) #打包信息
        time.sleep(3)
        print("------------------------------------休息3秒-------------------------------------")
    
    # 写入Excel
    write2excel()


# 打包信息
@retry(stop_max_attempt_number=3)
def pack_imformation(kinds_url,kinds_name):
    web_data = requests.get(kinds_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    selects = soup.select('div.sort.cl > div.sortC > dl > dd > a')
    # print(selects)

    namelist, linklist = [], []
    for i in selects:
        namelist.append(i.getText())
        linklist.append(i.get("href"))

    for name, pointlink in zip(namelist, linklist):
        # print( name, pointlink)
        try:
            province, city, lattitude, longitude = point_data(pointlink)
            print(name, kinds_name, province, city, lattitude, longitude)
            kinds_all_list.append([name, kinds_name, province, city, lattitude, longitude]) 
        except:
            pass
        

# 找到每个点的信息
def point_data(point_url):
    web_data = requests.get(point_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    names = soup.find_all('meta')
    text = names[2].get('content')       #province=四川;city=自贡;coord=104.76247,29.37363
    textregex = re.compile(r'province=(\S\S);city=(\S\S);coord=(\d+\W\d+),(\d+\W\d+)')
    mo = textregex.search(text)
    province,city,lattitude,longitude = mo.groups()
    # print(province,city,lattitude,longitude,sep='\n')
    return province,city,lattitude,longitude

# 写入Excel
def write2excel():
    os.chdir('D:\\tuba')
    wb = openpyxl.load_workbook('example.xlsx')
    sheet = wb['Sheet1']  # 选择一个excel页面
    print("234234")
    # 表格填入数据
    sheet.cell(row=1, column=1).value = "名称"
    sheet.cell(row=1, column=2).value = "类型"
    sheet.cell(row=1, column=3).value = "省名"
    sheet.cell(row=1, column=4).value = "市名"
    sheet.cell(row=1, column=5).value = "经度"
    sheet.cell(row=1, column=6).value = "纬度"

    for row in range(2, len(kinds_all_list)+2):
        sheet.cell(row=row, column=1).value = kinds_all_list[row-2][0]
        sheet.cell(row=row, column=2).value = kinds_all_list[row-2][1]
        sheet.cell(row=row, column=3).value = kinds_all_list[row-2][2]
        sheet.cell(row=row, column=4).value = kinds_all_list[row-2][3]
        sheet.cell(row=row, column=5).value = kinds_all_list[row-2][4]
        sheet.cell(row=row, column=6).value = kinds_all_list[row-2][5]
    wb.save('example.xlsx')
    print('已经下载数据')


main_url = 'http://poi.mapbar.com/liuzhou/'
kinds_all_list = []
kinds_data(main_url)

# kinds_all_list = [[1, 2, 3, 4, 5, 6], ['a', 'b', 'c', 'd', 'e', 'f']]
# write2excel()
