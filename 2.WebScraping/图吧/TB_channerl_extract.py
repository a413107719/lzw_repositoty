import requests, re, time, openpyxl, os
from bs4 import BeautifulSoup


# 找到各类型链接
def kinds_data(host_url):
    web_data = requests.get(host_url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    urls = soup.select('body > div.sort.cl > div > div > a')
    urlANDname_list = []
    for url in urls:
        kind2_name = url.get('title')
        kind2_url = url.get('href')
        urlandname = kind2_url + ',' + kind2_name
        urlANDname_list.append(urlandname)
    # print(urlANDname_list)
    # print(len(urlANDname_list))
    return urlANDname_list


# host_url = 'http://poi.mapbar.com/zigong/'
# kinds_data(host_url)
