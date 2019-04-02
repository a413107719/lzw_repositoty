# 可以完成爬取任务，后期需添加多线程、纵向和横向图片的分类保存
import requests
from bs4 import BeautifulSoup
import urllib.request

url = 'https://unsplash.com/'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text, 'lxml')
titles = soup.select('#gridMulti > div > div > div > figure > div > a')
links = soup.select('#gridMulti > div > div > div > figure > div > div > div._3dZoB > div._12slh > a')
sizes = soup.select('#gridMulti > div > div > div > figure > div > a > div > img')
# print(sizes)

i = 1
for link, size in zip(links, sizes):
    data = {
        'link': link.get('href'),
        'width': size.get(''),
    }
    imagepath = data['link']
    imagename = 'image'+str(i)
    f = open('D:\\imagesdownload\\' + imagename + '.jpg', 'wb')
    try:
        f = open('D:\\imagesdownload\\'+imagename+'.jpg', 'wb')
        f.write((urllib.request.urlopen(imagepath)).read())
        print(imagepath+' 下载完成')
        f.close()
    except Exception as e:
        print(imagepath + " error")
    i += 1


