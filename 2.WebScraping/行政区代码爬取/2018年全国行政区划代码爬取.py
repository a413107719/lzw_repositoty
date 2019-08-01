from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
from time import *


def get_html(url):
    global curr_url
    # user_agent = 'Mozilla/6.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.6796.99 Safari/537.36'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    response = urllib.request.Request(url)
    response.add_header('User-Agent', user_agent)
    response = urllib.request.urlopen(response, timeout=5)
    html = BeautifulSoup(response.read(), "html.parser", from_encoding='gbk')
    # print(html)
    return html


def get_area_list(url):
    try:
        html = get_html(url)
        tr_list = html.findAll('tr', {'class': 'provincetr'})
        for tr in tr_list:
            td_list = tr.findAll('td')
            for td in td_list:
                province_name = td.get_text()
                province_code = ''
                if td.a:
                    page = td.a.attrs['href']
                    index = page.index('.')
                    if index > -1:
                        substr = page[0:index]
                        province_code = substr + (12 - len(substr)) * '0'
                    pattern = re.compile(r'\w*.html')
                    province_url = re.sub(pattern, page, url)
                    print('\n' + str(province_code) + province_name + ': ' + province_url)
                    # 开始爬村镇信息
                    get_list(province_url, 5, province_code, province_name)

    except Exception as e:
        # 如果有出错，则回滚
        print(e)  # time out
        print('get_area_list重新请求！')
        sleep(3)
        get_area_list(url)




# get_level爬取到哪一级的数据 1省，2市，3区县，4，乡镇，5村,社区
def get_list(provinceurl, get_level, provincecode, provincename):
    try:
        # 获取市信息
        if get_level > 1:
            html = get_html(provinceurl)
            tr_list = html.findAll('tr', {'class': level_arr[str(2)]})
            for tr in tr_list:
                tempt_url = provinceurl
                td_list = tr.findAll('td')
                td = td_list[0]
                citytr_code = td_list[0].get_text()
                citytr_name = td_list[1].get_text()
                if td.a:
                    page = td.a.attrs['href']
                    pattern = re.compile(r'\w*.html')
                    city_url = re.sub(pattern, page, tempt_url)
                    # print(citytr_code, citytr_name, city_url)


                # 获取区县信息
                if get_level > 2:
                    html = get_html(city_url)
                    tempt_url = city_url
                    tr_list = html.findAll('tr', {'class':  level_arr[str(3)]})
                    for tr in tr_list:
                        td_list = tr.findAll('td')
                        td = td_list[0]
                        countytr_code = td_list[0].get_text()
                        countytr_name = td_list[1].get_text()
                        if td.a:
                            page = td.a.attrs['href']
                            pattern = re.compile(r'\w*.html')
                            countytr_url = re.sub(pattern, page, tempt_url)
                            # print(citytr_code,citytr_name,countytr_code,countytr_name,countytr_url,sep=' ')

                            # 获取乡镇信息
                            if get_level > 3:
                                html = get_html(countytr_url)
                                tempt_url2 = countytr_url
                                tr_list = html.findAll('tr', {'class': level_arr[str(4)]})
                                for tr in tr_list:
                                    td_list = tr.findAll('td')
                                    td = td_list[0]
                                    town_code = td_list[0].get_text()
                                    town_name = td_list[1].get_text()
                                    if td.a:
                                        page = td.a.attrs['href']
                                        pattern = re.compile(r'\w*.html')
                                        town_url = re.sub(pattern, page, tempt_url2)
                                        # print(citytr_code, citytr_name, countytr_code, countytr_name, town_code, town_name,town_url, sep=' ')

                                        # 获取村、社区信息
                                        if get_level > 4:
                                            html = get_html(town_url)
                                            tempt_url3 = town_url
                                            tr_list = html.findAll('tr', {'class': level_arr[str(5)]})
                                            # print(tr_list)
                                            for tr in tr_list:
                                                td_list = tr.findAll('td')
                                                td = td_list[0]
                                                village_code = td_list[0].get_text()
                                                village_number = td_list[1].get_text()
                                                village_name = td_list[2].get_text()
                                                if td.a:
                                                    page = td.a.attrs['href']
                                                    pattern = re.compile(r'\w*.html')
                                                    village_url = re.sub(pattern, page, tempt_url3)
                                                    print(provincecode, provincename, citytr_code, citytr_name, countytr_code, countytr_name, town_code, town_name, village_code, village_number, village_name, village_url, sep=' ')
                                                else:
                                                    print(provincecode, provincename, citytr_code, citytr_name, countytr_code, countytr_name, town_code, town_name, village_code, village_number, village_name, "null page")
                                                    # todo:写入excel

                                    else:
                                        print(provincecode, provincename, citytr_code, citytr_name, countytr_code, countytr_name, town_code, town_name, "null page")
                                        # todo:写入excel
                                    sleep(2)

                        else:
                            print(provincecode, provincename, citytr_code,citytr_name,countytr_code,countytr_name,"null page")
                            # todo:写入excel
                    sleep(3)

    except Exception as e:
        # 如果有出错，则回滚
        print(e)  # time out
        print('重新请求！')
        sleep(3)
        get_list(provinceurl, get_level, provincecode, provincename)


url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'
curr_url = ''
level_arr = {'1': 'provincetr', '2': 'citytr', '3': 'countytr', '4': 'towntr', '5': 'villagetr'}
get_area_list(url)


# # url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/13.html"  #河北
# url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/11.html"   #北京
# get_list(url, 5)