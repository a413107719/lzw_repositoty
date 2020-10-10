# -*- coding=UTF-8 -*-
import arcpy
'''
    本脚本主要用于多个文件夹里有相同名称的shp数据的合并，如：
    'F:\\g48c001002\\aanp.shp', 'F:\\g48c001003\\aanp.shp', 
    'F:\\g48c001002\\agnp.shp', 'F:\\g48c001003\\agnp.shp'
'''


folder = r'F:\测试数据\区域地理信息'
shpfolder = r'F:\测试数据\shpfolder'

arcpy.env.workspace = folder
subfolder = arcpy.ListFiles()
print(subfolder)

# 读取文件夹中一共有哪些同名数据
shplist = []
for fol in subfolder:
    arcpy.env.workspace = folder + '\\' + fol
    files = arcpy.ListFeatureClasses()
    # print(files)
    for f in files:
        if f not in shplist:
            shplist.append(f)
print(shplist)

# 创建字典,并构建需要合并的同名数据的具体路径
dictionary = {}
for shp in shplist:
    dictionary[shp] = []
    for fol in subfolder:
        arcpy.env.workspace = folder + '\\' + fol
        files = arcpy.ListFeatureClasses()
        if shp in files:
            dictionary[shp].append(folder + '\\' + fol + '\\' + shp)

# 合并数据
for key in dictionary.keys():
    li = dictionary[key]
    print('正在合并要素：', li)
    arcpy.Merge_management(li, shpfolder + '\\' + key + '.shp')
