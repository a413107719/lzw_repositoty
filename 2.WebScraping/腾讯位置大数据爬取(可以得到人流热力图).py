# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 00:45:20 2018
@author: 武状元
"""
import requests
import json
import pandas as pd
import time


def get_TecentData(count=4, rank=0):  # 先默认为从rank从0开始
    url = 'https://xingyun.map.qq.com/api/getXingyunPoints'
    locs = ''
    paload = {'count': count, 'rank': rank}
    response = requests.post(url, data=json.dumps(paload))
    datas = response.text
    dictdatas = json.loads(datas)  # dumps是将dict转化成str格式，loads是将str转化成dict格式
    time = dictdatas["time"]  # 有了dict格式就可以根据关键字提取数据了，先提取时间
    print(time)
    locs = dictdatas["locs"]  # 再提取locs（这个需要进一步分析提取出经纬度和定位次数）
    locss = locs.split(",")
    # newloc=[locss[i:i+3] for i in range(0,len(locss),3)]
    temp = []  # 搞一个容器
    for i in range(int(len(locss) / 3)):
        lat = locss[0 + 3 * i]  # 得到纬度
        lon = locss[1 + 3 * i]  # 得到经度
        count = locss[2 + 3 * i]

        # todo 需声明需要爬取的经纬度范围，以避免数据量过大
        if 3115 < int(lat) < 3270 and 11823 < int(lon) < 11930:
            temp.append([time, int(lat) / 100, int(lon) / 100, count])  # 容器追加四个字段的数据：时间，纬度，经度和定位次数

    result = pd.DataFrame(temp)  # 用到神器pandas，真好用
    result.dropna()  # 去掉脏数据，相当于数据过滤了
    result.columns = ['time', 'lat', 'lon', 'count']
    result.to_csv('TecentData.txt', mode='a', index=False)  # model="a",a的意思就是append，可以把得到的数据一直往TecentData.txt中追加


# 基于腾讯位置大数据平台的全球移动定位数据Python爬取与清洗
# https://blog.csdn.net/qq_32231883/article/details/85234614?tdsourcetag=s_pctim_aiomsg
if __name__ == '__main__':
    while (1):  # 一直循环吧，相信我，不到一小时你电脑硬盘就要炸，大概速度是一分钟一百兆数据就可以爬下来
        for i in range(4):
            get_TecentData(4, i)  # 主要是循环count，来获取四个链接里的数据