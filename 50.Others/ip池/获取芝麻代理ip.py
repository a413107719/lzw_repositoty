import requests


# 获取代理列表
def get_ip_list():
    print("正在获取代理列表...")
    url="http://http.tiqu.alicdns.com/getip3?num=1&type=3&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=2&sb=0&pb=4&mr=1&regions=" #从代理网站上获取的url
    page = requests.get(url)
    iplist = page.text
    ip_list = iplist.split('</br>')
    print(len(ip_list)-1)
    if len(ip_list)==1:
        print("ip获取失败")
    print("代理列表抓取成功……")
    return ip_list[:-1]


# 格式化ip，获取一个proxise
def get_proxies(ip):
    proxy_ip = 'http://' + ip
    proxies = {'http': proxy_ip}
    return proxies


ip = get_ip_list()[0]
proxies = get_proxies(ip)


