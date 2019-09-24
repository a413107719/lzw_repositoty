import arcpy
import os
import shutil


folder = 'F:\\测试数据\\全国基础地理信息测试数据\\'

# 循环得到folder里的gdb，得到数据列表
gdbs = os.listdir(folder)
print("包含GDB：" + str(gdbs) + '\n')
gdbfeaturelist = []    # ['F:\\全国基础地理信息测试数据\\H48.gdb',['RESP', 'RESA',  'HYDP', 'HYDL']]
for gdb in gdbs:
    gdbpath = folder + gdb
    arcpy.env.workspace = gdbpath
    shplist = arcpy.ListFeatureClasses()
    # print(shplist)
    gdbfeaturelist.append([gdbpath, shplist])
    # break

# 循环数据列表，找到相同数据名称的数据,构造字典 如:RESP ['F:\\测试数据\\全国基础地理信息测试数据\\H48.gdb\\RESP', 'F:\\测试数据\\全国基础地理信息测试数据\\H49.gdb\\RESP'....]
dic = {}
for i in gdbfeaturelist:
    print(i)
    for featurename in i[1]:
        if featurename not in dic:
            dic[featurename] = [i[0] + '\\' + featurename]
        else:
            dic[featurename].append(i[0] + '\\' + featurename)

for key, value in dic.items():
    print(key, value)


# 创建输出gdb
gdbpath = folder + '\\' + "gdbmerge.gdb"
arcpy.env.workspace = folder
if arcpy.Exists("gdbmerge.gdb"):
    shutil.rmtree(gdbpath)
    print('gdbmerge.gdb数据库已存在,将删除')
arcpy.CreateFileGDB_management(folder, "gdbmerge.gdb")
print("成功创建gdbmerge.gdb数据库")

# merge数据
for key in dic.keys():
    dic[key].reverse()
    arcpy.env.workspace = gdbpath
    arcpy.Merge_management(dic[key], gdbpath + '\\' + key)
    print("Finish Merge：", key, dic[key])
print("--------------------------合并数据已完成------------------------", '\n')