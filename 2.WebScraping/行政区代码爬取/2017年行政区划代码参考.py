# # 可以完成爬取任务，后期需添加多线程、纵向和横向图片的分类保存
# import requests
# from bs4 import BeautifulSoup
# import urllib.request
#
# s = requests.Session()
# s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
# s.headers['Host'] = 'http://www.stats.gov.cn'
# url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'
# r = s.get(url)
# r.encoding = 'utf-8'
# print(r.text)
#
# # soup = BeautifulSoup(web_data.text, 'lxml')
# # print(soup)


import requests
from lxml import etree

class Spider():
    def __init__(self):
        self.province = ''
        self.province_code = ''
        self.city = ''
        self.city_code = ''
        self.district = ''
        self.district_code = ''

        self.committee=''
        self.committee_code=''
        self.committee_code2=''

        self.city_url = ''
        self.district_url = ''
        self.url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'

        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }


    def get_province(self):
        """省"""
        rep = requests.get(url=self.url, headers=self.headers)
        html = rep.content
        html = etree.HTML(html)

        data=html.xpath('//tr[@class="provincetr"]/td')[0]
        province_url = data.xpath('//a/@href')
        province_url.pop(-1)
        print('###################')
        print(province_url)
        province_name = data.xpath('//a/text()')

        for i in range(len(province_name)):
            province_code = province_url[i][:2]
            self.province = province_name[i]
            print(self.province)
            self.province_code = province_code
            self.city_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/" + self.province_code+'.html'
            print("省："+self.city_url)
            self.get_city()


    def get_city(self):
        """市"""

        rep = requests.get(url=self.city_url, headers=self.headers)
        html = rep.content
        html = etree.HTML(html)


        city_url=html.xpath('//tr[@class="citytr"]/td//a/@href')
        city_data = html.xpath('//tr[@class="citytr"]/td//a/text()')

        city_url = list(set(city_url))
        print(city_url)


        city = city_data[1::2]
        city_code = city_data[::2]

        for i in range(len(city_code)):
            city_code_s = city_code[i][:4]
            self.city = city[i]
            self.city_code = city_code_s
            self.district_url = self.url+ '/' + city_url[i]

            print("市："+self.district_url)
            self.get_district(self.district_url)


    def get_district(self,url):
        """区"""
        rep = requests.get(url=url, headers=self.headers)
        html = rep.content
        html = etree.HTML(html)

        district_data = html.xpath('//tr[@class="countytr"]/td//a/text()')
        district_url=html.xpath('//tr[@class="countytr"]/td//a/@href')
        district_url=list(set(district_url))

        district = district_data[1::2]
        district_code = district_data[::2]

        for i in range(len(district)):
            self.district = district[i]
            self.district_code = district_code[i][:6]

            self.qu_url=self.city_url[:-5] + '/' +district_url[i]

            print("区："+self.qu_url)
            self.get_zhen(self.qu_url)

    def get_zhen(self,url):
        "镇街道"
        rep=requests.get(url=url,headers=self.headers)
        html=rep.content
        html=etree.HTML(html)

        zhen_data=html.xpath('//tr[@class="towntr"]/td//a/text()')
        zhen_url=html.xpath('//tr[@class="towntr"]/td//a/@href')

        zhen_url = list(set(zhen_url))

        zhen=zhen_data[1::2]
        zhen_code=zhen_data[::2]

        for i in range(len(zhen)):

            self.zhen=zhen[i]
            self.zhen_code=zhen_code[i][:8]


            quwei_url2=self.qu_url
            quwei_url=quwei_url2[:url.rindex("/")]+'/'+zhen_url[i]
            print("镇："+quwei_url)
            self.get_quwei(quwei_url)

    def get_quwei(self,url):
        """区委"""
        rep=requests.get(url=url,headers=self.headers)
        html=rep.content
        html=etree.HTML(html)

        quwei_data=html.xpath('//tr[@class="villagetr"]/td/text()')

        quwei=quwei_data[2::3]
        step=3
        quwei_d=[quwei_data[i:i+step] for i in range(0,len(quwei_data),step)]


        for i in range(len(quwei)):
            self.quwei=quwei_d[i][2]
            self.quwei_code1=quwei_d[i][1]
            self.quwei_code2=quwei_d[i][0]

            self.write_data()


    def write_data(self):
        data = self.province + ',' + self.province_code + ',' + self.city + ',' + self.city_code + ',' + self.district + ',' + self.district_code + ',' + self.zhen + ',' + self.zhen_code + ',' + self.quwei + ',' + self.quwei_code1 + ',' + self.quwei_code2 + '\n'

        with open('data_mkiceman.txt', 'a', encoding='utf8') as f:
            f.write(data)

if __name__ == '__main__':
    spider = Spider()
    spider.get_province()