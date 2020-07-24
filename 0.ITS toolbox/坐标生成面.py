# -*- coding=UTF-8 -*-
import pandas as pd

'''
坐标格式为：
1,36620144.5239,3500980.1509,2,36620053.1823,3500943.4449,
3,36620018.1826,3500980.048,4,36620091.2476,3501014.5299
'''

excel = "F:\\巫溪\\巫溪县历史遗留及关闭矿山损毁土地现状调查及复垦计划表.xls"
idcolumn = '地块编号'
coordcolumn = '四至坐标'

# 显示数据框格式
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 2000)

# 读取数据
df = pd.read_excel(excel, header=0)
# newdf = df  # newdf = df.loc[:, [idcolumn, coordcolumn]]
newdf = df.loc[:, [idcolumn, coordcolumn]]

# 替换特殊字符
newdf[coordcolumn] = newdf[coordcolumn].str.replace('，', ',')
newdf[coordcolumn] = newdf[coordcolumn].str.replace(',,', ',')
newdf[coordcolumn] = newdf[coordcolumn].str.replace('\n', '')

# 构造经纬度
for i in range(len(newdf)):
    # value = newdf.loc[i][1]
    value = newdf.loc[i][coordcolumn]
    valuelist = str(value).split(',')
    pointlist = []
    x = 0
    while x < len(valuelist):
        pointlist.append(valuelist[x+1] + '#' + valuelist[x+2])
        x += 3
    newdf.loc[i, '坐标1'] = str(pointlist).replace('[', '').replace('\'', '').replace(']', '')

del newdf[coordcolumn]
df2 = newdf.drop('坐标1', axis=1).join(newdf['坐标1'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('坐标'))
df2['x'], df2['y'] = df2['坐标'].str.split('#', 1).str
df2[['x', 'y']] = df2[['x', 'y']].apply(pd.to_numeric)
df2 = df2.reset_index()
del df2['坐标']
del df2['index']


import arcpy
import numpy as np
arcpy.env.overwriteOutput = True
outputpointpath = "C:\\Users\\lzw_ghy\\Documents\\ArcGIS\\Projects\\MyProject\\MyProject.gdb\\testPoin88t"

ra = df2.to_records(index=False)
np_array = np.asarray(ra)
print(np_array.dtype)
arcpy.da.NumPyArrayToFeatureClass(np_array, outputpointpath, ['x', 'y'])