import random
import requests
from bs4 import BeautifulSoup
import re
import time
import urllib
import urllib.request

def get_proxy(page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    res = requests.get('https://www.xicidaili.com/nn/%d' % page, headers=headers)
    print(res.status_code == requests.codes.ok)
    urltext = res.text
    soup = BeautifulSoup(urltext, 'lxml')

    proxy_list = []
    trlist = soup.select('tr[class="odd"]')
    for i in trlist:
        ip = re.compile(r'\d+\.\d+\.\d+\.\d+').search(str(i)).group()
        port = re.compile(r'<td>\d+</td>').search(str(i)).group().split('>')[1].split('<')[0]
        proxy = '%s:%s' % (ip, port)
        proxy_list.append(proxy)
    read_proxy(proxy_list)

def read_proxy(proxy_list):
    print('开始测试')
    for proxy in proxy_list:
        print()
        print("当前代理IP：%s" % proxy)
        sleeptime = random.randint(1,3)
        # print("等待%s秒" % sleeptime)
        time.sleep(sleeptime)

        proxt_suport = urllib.request.ProxyHandler({'http':proxy})
        opener = urllib.request.build_opener(proxt_suport)
        urllib.request.install_opener(opener)

        req = urllib.request.Request('http://httpbin.org/ip')  # 这个网址可以返回本机ip地址
        try:
            html = urllib.request.urlopen(req).read()
            print(html)
            print('打开成功')
            list.append(proxy)
        except Exception as e:
            # print(e)
            print('打开失败')


if __name__ == '__main__':
    canuseport =[]
    list = []
    for i in range(1, 4):  # 设置需要爬取的页面
        get_proxy(i)
    print("首次爬取能用的端口包括：")
    print(list)
    canuseport = list

    for i in range(3):
        list = []
        read_proxy(canuseport)
        print('第 %d 次验证，能用的端口包括：%s' % (i+1, str(list)))
        canuseport = list
    print('最终能用的端口包括：')
    print(canuseport)
