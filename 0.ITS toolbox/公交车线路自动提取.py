from GD_address2point import findXY
import pandas as pd
from pandas import DataFrame
import numpy as np
import pandas as pd
import os
from lxml import etree
import pymongo


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',1000)
excel = "F:\\测试数据\\公交线路信息.xlsx"
df = pd.read_excel(excel)
# print(df.columns)
# print(df.head(3))

client = pymongo.MongoClient('localhost', 27017)
mydb = client['zkStudio']
mycolumn = mydb['gongjaoxy']

df1 = df.drop(['站点信息'], axis=1).join(df['站点信息'].str.split('\n', expand=True).stack().reset_index(level=1, drop=True).rename('公交站名'))
df1["去返程"],df1['公交站'] = df1['公交站名'].str.split('：',1).str
del df1["公交站名"]
df2 = df1.reset_index(drop=True)
df3 = df2.drop(['公交站'], axis=1).join(df2['公交站'].str.split('、', expand=True).stack().reset_index(level=1, drop=True).rename('公交站'))
df4 = df3.reset_index(drop=True)

df4["newname"] =None
df4["longitude"] =None
df4["lattitude"] =None
df4["level"] =None

pointvalues = {}
for i in range(len(df4["公交站"])):
    stationname = df4.iloc[i][12]
    # print(stationname)
    newname = "新都区"+ stationname.replace('站', '公交站')
    print(newname)

    # mongodb查重
    findresult = mycolumn.find({"name": newname})
    num = len(list(findresult))
    if num == 1:
        # 已经存在
        find = mycolumn.find_one({"name": newname})
        longitude, lattitude, level = find['longitude'], find['lattitude'], find['level']
        print("yes", newname, longitude, lattitude, level, sep=' ')
    else:
        longitude, lattitude, level = findXY('成都市', newname)
        # print(newname, longitude, lattitude, level, sep=' ')
        print('No', newname, longitude, lattitude, level)
        pointvalues[newname] = longitude, lattitude, level

        # 写入mongodb
        dict = {"name": newname, "longitude":longitude,"lattitude":lattitude, "level":level}
        mycolumn.update(dict, dict, True)

    # 写入pandas
    df4.iloc[i, 13] = newname
    df4.iloc[i, 14] = longitude
    df4.iloc[i, 15] = lattitude
    df4.iloc[i, 16] = level

print(df4.head())
df4.to_csv("F:\\测试数据\\公交线路信息t.csv",encoding = "utf_8_sig")


