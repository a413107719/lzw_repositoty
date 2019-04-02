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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    def get_province(self):
        """省"""
        rep = requests.get(url=self.url, headers=self.headers)
        html = rep.content
        html = etree.HTML(html)
        province_link_list = html.xpath('//tr[@class="provincetr"]/td/a/@href')
        province_name_list = html.xpath('//tr[@class="provincetr"]/td/a/text()')
        print(province_link_list)
        print(province_name_list)

        for i in range(len(province_name_list)):
            self.province = province_name_list[i]
            self.city_url = self.url + province_link_list[i]
            print(self.province)
            print(self.city_url)
            self.get_city()

    def get_city(self):
        """市"""
        # test1
        pass


    def get_strict(self):
        """区县"""


    def get_town(self):
        """镇或街道"""
        pass


    def get_community(self):
        """社区"""
        pass


    def write_data(self):
        pass

if __name__ == '__main__':
    spider = Spider()
    spider.get_province()
