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
        "Cookie":"SINAGLOBAL=1287367784314.3706.1534338927653; login_sid_t=2519fc0720c4cc00eaad2d3a81bfa000; cross_origin_proto=SSL; _s_tentry=www.baidu.com; Apache=6155613144806.95.1557927005330; ULV=1557927005343:12:2:2:6155613144806.95.1557927005330:1557767521416; un=lzw19910@qq.com; wvr=6; Hm_lvt_e60c55838acbc89c7409eced091b4723=1557927002; Hm_lvt_53d94eb4421c8445dba94dfb21a76732=1557927002; WBStorage=e4e08ad1044aa883|undefined; WBtopGlobal_register_version=5c10f3128cf400c5; un=lzw19910@qq.com; SSOLoginState=1557931312; ALF=1589467341; SCF=ApVpeN6coXY20IZoTUReJhzcsBNF_im0u-APHuZSRmSZdQ_FcO5QHfn5pMVOY1UN1c3MTr2Vkzj50v9yH57spdk.; SUB=_2A25x2FUADeRhGeBO7VUX-CjLzT6IHXVSrMHIrDV8PUNbmtAKLWbGkW9NRdri1Z8YUewUFnsS61inZ8HdlBMey2s_; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF4or_iefBEcLZ3PFfEA-U05JpX5KzhUgL.Foq7SoMc1hqNSoz2dJLoI7RLxKqL1-BL12-feKeRentt; SUHB=0OM0tmaYDZDkdn; Hm_lvt_e60c55838acbc89c7409eced091b4723=1557927002,1557931348; Hm_lvt_53d94eb4421c8445dba94dfb21a76732=1557927002,1557931348; UOR=f.uliba.net,widget.weibo.com,graph.qq.com; Hm_lpvt_e60c55838acbc89c7409eced091b4723=1557931607; Hm_lpvt_53d94eb4421c8445dba94dfb21a76732=1557931607; Hm_lpvt_e60c55838acbc89c7409eced091b4723=1557931801; Hm_lpvt_53d94eb4421c8445dba94dfb21a76732=1557931801; webim_unReadCount=%7B%22time%22%3A1557931927852%2C%22dm_pub_total%22%3A0%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D",
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
        html_1 = "https://s.weibo.com/article?q=周杰伦&Refer=weibo_article&page="+str(page)
        get_content(html_1)
