# 待完成，不明确问题
import requests
from bs4 import BeautifulSoup

#主函数
def main_fuction(main_url, single_cates_url):
    if single_cates_url is not '':
        shops_url = main_url + single_cates_url
        get_shops(shops_url)
    else:
        get_all_cates(main_url)

#todo:抓取所有分类
def get_all_cates(main_url):
    pass




def get_shops(shops_url):
    print(shops_url)
    webdata = requests.get(shops_url)
    soup = BeautifulSoup(webdata.text, 'lxml')
    inputs_text(inputs_main)

def inputs_text(inputs):
    for i in inputs:
        text = str(i[0])
        text = soup.select(i[1])
        for y in text:
            print(i[0] + ': ' + str(y[i[2]]))

    筛选信息
    names = soup.select('tiaojian')
    titles = soup.select('tiaojian')
    single_shop_url = soup.select('src')
    for name, title in zip(names, titles):
        data = {
            'name': name.get_text(),
            'title': title.get('title'),
            'single_shop_url' : single_shop_url.get('src'),
        }
        get_imformation(single_shop_url,data)




#todo:抓取单条商店信息（名称，地址，经纬度，评分，电话等）
def get_imformation(single_shop_url,data):
    print(single_shop_url,data)


# ----------------------------------------------------------------------------------------------------
# 参数
main_url = 'http://nanchuan.meituan.com/'   #填入主网址
single_cates_url = 'meishi/'                 #如果需要爬取某一种类数据，填入相关值
inputs_main = [
    ['title', '#gridMulti > div > div > div > figure > div > div > div._3dZoB > div._12slh > a', 'class'],
    ['link', '#gridMulti > div > div > div > figure > div > div > div._3dZoB > div._12slh > a', 'href']
]
inputs_sub = []

# 主函数
main_fuction(main_url, single_cates_url)




