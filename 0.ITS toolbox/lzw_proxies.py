# -*- coding=UTF-8 -*-
import requests, time
import random


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
def change_proxies(proxies_list):
    ip = random.sample(proxies_list, 1)[0]
    proxie_ip = {'https': ip}   # 写成https就能爬取了，不知道tmd什么原因
    print(proxie_ip)
    return proxie_ip
