from bs4 import BeautifulSoup
import requests,os


def get_pagetext(url, dirc):
    web_data = requests.get(url)
    source = BeautifulSoup(web_data.text,'lxml')       
    title = source.select('div > div.text-head > h3')
    section_text = source.select('div > div > p')
    titlename = title[0].text

#store the page into text
    os.makedirs(dirc)
    os.chdir(dirc)        #将储存位置设置为当前目录
    txtfile = open('%s.txt'%titlename, "ab+")
    txtfile.write((titlename + '\r\n').encode('UTF-8'))  # 题目需要转换为utf-8编码，否则会出现乱码
    for i in section_text:
        txtfile.write((i.text + '\r\n').encode('UTF-8'))
    print("%s 已下载"%titlename)
    txtfile.close()



#Todo:get pagesURL，没有弄成功
# chapters = source.find_all('ul',class_='cf')          #不知道返回的是什么值，要用str()函数转为可读信息
# download_soup = BeautifulSoup(str(chapters),'lxml')
# for name in download_soup.find_all('a'):
#     print('https:'+name.get('href'))

# main function
url = 'https://read.qidian.com/chapter/_AaqI-dPJJ4uTkiRw_sFYA2/eSlFKP1Chzg1'
dirc1 = "D:\\book"           #储存位置
get_pagetext(url, dirc1)


#现在只能爬某一章节的文档，不能整本爬取。