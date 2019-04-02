import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup

# 找到各类型链接
def kinds_data(point_url):
    web_data = requests.get(point_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    titles = soup.select('body > div.sort.cl > div > div > a')
    kinds_urls = soup.select('body > div.sort.cl > div > div > a')
    for title,kinds_url in zip(titles,kinds_urls):
        kinds_name = title.string
        each_url  = kinds_url.get('href')
        pack_imformation(each_url,kinds_name) #打包信息
        time.sleep(3)
        print("------------------------------------休息3秒-------------------------------------")

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

# 打包信息
def pack_imformation(each_url,kinds_name):
    # url = 'http://poi.mapbar.com/zigong/FC0/'
    web_data = requests.get(each_url)
    soup = BeautifulSoup(web_data.text,'lxml')
    names = soup.select('body > div.sort.cl > div.sortC > dl > dd > a')
    links = soup.select('body > div.sort.cl > div.sortC > dl > dd > a')
    # print(names)
    ID = 1
    for name, link in zip(names, links):
        point_url = link.get('href')
        try:
            province, city, lattitude, longitude = point_data(point_url) #找到每个点信息
            # 设置表格路径
            os.chdir('C:\\Users\\lzw19\\Desktop')
            wb = openpyxl.load_workbook('example.xlsx')
            sheet = wb['地名爬取']  # 选择一个excel页面
            # 表格填入数据
            max_row = sheet.max_row
            newrow = max_row + 1
            sheet.cell(row=newrow, column=1).value = ID
            sheet.cell(row=newrow, column=2).value = name.string
            sheet.cell(row=newrow, column=3).value = province
            sheet.cell(row=newrow, column=4).value = city
            sheet.cell(row=newrow, column=5).value = lattitude
            sheet.cell(row=newrow, column=6).value = longitude
            sheet.cell(row=newrow, column=7).value = kinds_name
            wb.save('example.xlsx')
            print('已经下载数据：' + name.string + '  '+ kinds_name)
            ID += 1
        except:
            pass





# 执行主函数
main_url = 'http://poi.mapbar.com/zigong/'
kinds_data(main_url)