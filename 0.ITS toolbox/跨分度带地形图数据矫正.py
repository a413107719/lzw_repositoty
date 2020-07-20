import arcpy
import shutil
import os


# 参数
gdbpath = r'F:\测试数据\test\testgdb1.gdb'    # 数据源
fanwei = "F:\\测试数据\\test\\data.gdb\\fanwei"
firstprojection = r'F:\巫溪\CGCS2000_GK_CM_108E.prj'
newprojection = r'F:\巫溪\CGCS2000 GK CM 111E.prj'

gdbname = gdbpath.split('\\')[-1]
foldername = gdbpath.split(gdbname)[0]
temptpath = foldername + 'tempt.gdb'
mergefilefolder = foldername + 'shpfolder' + '\\'
arcpy.env.workspace = foldername
if arcpy.Exists("tempt.gdb"):
    shutil.rmtree(temptpath)
    print('tempt.gdb数据库已存在,将删除')
arcpy.CreateFileGDB_management(foldername, "tempt.gdb")
print("成功创建tempt.gdb数据库")
if os.path.isdir(mergefilefolder):
    shutil.rmtree(mergefilefolder)
    print('mergefolder已存在,将删除')
os.makedirs(mergefilefolder)

arcpy.env.workspace = gdbpath
arcpy.env.overwriteOutput = True
featurelist = arcpy.ListFeatureClasses()
print(featurelist)

for feature in featurelist:
    featurepath = gdbpath + '\\' + feature
    featurepath108 = temptpath + '\\' + feature + '108'
    arcpy.CopyFeatures_management(featurepath, featurepath108)
    arcpy.DefineProjection_management(featurepath, newprojection)
    arcpy.DefineProjection_management(featurepath108, firstprojection)
    featurepath108to111 = featurepath108 + 'to111'
    arcpy.Project_management(featurepath108, featurepath108to111, newprojection)

    # 合并要素
    mergefile = mergefilefolder + feature + '.shp'
    arcpy.Merge_management(inputs=[featurepath, featurepath108to111], output=mergefile, add_source="NO_SOURCE_INFO")

    # 删除范围以外的要素
    Layer_With_Selection, Output_Layer_Names, Count = arcpy.SelectLayerByLocation_management(in_layer=[mergefile],
    overlap_type="INTERSECT", select_features=fanwei, search_distance="", selection_type="NEW_SELECTION",invert_spatial_relationship="NOT_INVERT")
    Updated_Input_With_Rows_Removed = arcpy.DeleteRows_management(in_rows=Layer_With_Selection)[0]
    print('%s处理完成'%(feature))







