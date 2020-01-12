# coding:utf-8
import requests
import json
import re
from bs4 import BeautifulSoup


# 爬起文章页面
def get_content(html_1):
    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Cookie":"SINAGLOBAL=1287367784314.3706.1534338927653; un=lzw19910@qq.com; wvr=6; un=lzw19910@qq.com; Hm_lvt_e60c55838acbc89c7409eced091b4723=1557927002,1557931348; Hm_lvt_53d94eb4421c8445dba94dfb21a76732=1557927002,1557931348; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF4or_iefBEcLZ3PFfEA-U05JpX5KMhUgL.Foq7SoMc1hqNSoz2dJLoI7RLxKqL1-BL12-feKeRentt; ALF=1589701303; SSOLoginState=1558165305; SCF=ApVpeN6coXY20IZoTUReJhzcsBNF_im0u-APHuZSRmSZIUAY7kTaL4r046dodTy_51StDU3Lp_urvYQcsRCQm64.; SUB=_2A25x28dqDeRhGeBO7VUX-CjLzT6IHXVSkL-irDV8PUNbmtAKLU3nkW9NRdri1VL72Z-KAnt92MEA7BAHLREqL9LY; SUHB=0gHyyQNi_XOuK9; _s_tentry=login.sina.com.cn; UOR=f.uliba.net,widget.weibo.com,login.sina.com.cn; Apache=1379466278776.8286.1558165309153; ULV=1558165309453:13:3:3:1379466278776.8286.1558165309153:1557927005343; WBStorage=53830d4156ad61ab|undefined; Hm_lvt_e60c55838acbc89c7409eced091b4723=1557927002,1557931348; Hm_lpvt_e60c55838acbc89c7409eced091b4723=1558165321; Hm_lvt_53d94eb4421c8445dba94dfb21a76732=1557927002,1557931348; Hm_lpvt_53d94eb4421c8445dba94dfb21a76732=1558165321",
        "Host":"s.weibo.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

    }
    get_text = requests.get(html_1, headers=header)
    soup_text = BeautifulSoup(get_text.text,features="lxml")
    article_title1 = soup_text.select("div > div > h3 > a")
    for i in article_title1:
        link = i['href']
        title = i['title']
        print(title,link,sep=': ')


if __name__=="__main__":
    page_num = 50
    for page in range(1,page_num):
        html_1 = "https://s.weibo.com/article?q=达州&Refer=weibo_article&page="+str(page)
        get_content(html_1)
