import arcpy

# 添加需要提取的要素列表
# Todo: 替换为从excel模板总提取数据及其条件
point_table = [
    ["高程点", "Layer = 'GCD'"]
]

polyline_table = [
    ["等高线", "Layer = 'DGX'"],
    ["建筑轮廓", "Layer = 'JMD'"],
    ["陡坎斜坡", "Layer = 'DMTZ'"],
    ["管线注记及附属设施", "Layer = 'GXYZ'"],
    ["道路设施", "Layer = 'DLSS'"],
    ["河流湖泊", "Layer = 'SXSS'"],
    ["路灯", "Layer = 'DLDW' And RefName = 'gc097'"],
    ["坟", "Layer = 'DLDW' And RefName = 'gc111'"],
    ["植被", "Layer = 'ZBTZ' "]
]

polygon_table = [

]

annotation_table = [
    ["建筑注记", "Layer = 'JMD'"],
    ["小地名", "Layer = 'ZJ'"]
]


# 新建一个output数据库
def create_gdb():
    if arcpy.Exists("ProjectGDB.gdb"):
        print('ProjectGDB.gdb数据库已存在,将直接把数据写入数据库')
    else:
        arcpy.CreateFileGDB_management(input_folder, "ProjectGDB.gdb")
        print("成功创建ProjectGDB.gdb数据库")


# 找到所有dwg文件，并提取信息到数据库
def dwg2gdb(feature_point, feature_polyline, feature_polygon, feature_annotation):
    fcs = arcpy.ListFiles("*.dwg")
    for fc in fcs:
    
        # 提取点数据
        dwg_point = input_folder + fc + "\\Point"
        for feature in feature_point:
            # 有相同文件名自动添加后缀
            arcpy.env.workspace = output_folder
            featurename = feature[0]
            i = 1
            while True:
                if arcpy.Exists(featurename):
                    print("数据库中存在数据名：%s" % featurename)
                    featurename = feature[0] + str(i)
                    i += 1
                    continue
                else:
                    break
            # 提取要素
            arcpy.FeatureClassToFeatureClass_conversion(dwg_point, output_folder, featurename, feature[1])
            print("成功在数据库中添加要素：" + featurename)
        print("点数据已提取完成" + "\n")
    
        # 提取线数据
        dwg_polyline = input_folder + fc + "\\Polyline"
        for feature in feature_polyline:
            # 有相同文件名自动添加后缀
            arcpy.env.workspace = output_folder
            featurename = feature[0]
            i = 1
            while True:
                if arcpy.Exists(featurename):
                    print("数据库中存在数据名：%s" % featurename)
                    featurename = feature[0] + str(i)
                    i += 1
                    continue
                else:
                    break
            # 提取要素
            arcpy.FeatureClassToFeatureClass_conversion(dwg_polyline, output_folder, featurename, feature[1])
            print("成功在数据库中添加要素：" + featurename)
        print("线数据已提取完成" + "\n")

        # 提取面数据
        dwg_polygon = input_folder + fc + "\\Polygon"
        for feature in feature_polygon:
            # 有相同文件名自动添加后缀
            arcpy.env.workspace = output_folder
            featurename = feature[0]
            i = 1
            while True:
                if arcpy.Exists(featurename):
                    print("数据库中存在数据名：%s" % featurename)
                    featurename = feature[0] + str(i)
                    i += 1
                    continue
                else:
                    break
            # 提取要素
            arcpy.FeatureClassToFeatureClass_conversion(dwg_polygon, output_folder, featurename, feature[1])
            print("成功在数据库中添加要素：" + featurename)
        print("面数据已提取完成" + "\n")
    
        # 提取注记
        dwg_annotation = input_folder + fc + "\\Annotation"
        for feature in feature_annotation:
            # 有相同文件名自动添加后缀
            arcpy.env.workspace = output_folder
            featurename = feature[0]
            i = 1
            while True:
                if arcpy.Exists(featurename):
                    print("数据库中存在数据名：%s" % featurename)
                    featurename = feature[0] + str(i)
                    i += 1
                    continue
                else:
                    break
            # 提取要素
            arcpy.FeatureClassToFeatureClass_conversion(dwg_annotation, output_folder, featurename, feature[1])
            print("成功在数据库中添加注记要素：" + featurename)
        print("注记已提取完成" + "\n")


# 新建map + 添加数据 + 可视化
def data_visualization(output_f):
    pass


input_folder = 'F:\\测试数据\\地形图信息提取\\'     # 以后替换为 input_folder = arcpy.GetParameterAsText(0)
output_folder = input_folder + "ProjectGDB.gdb"
arcpy.env.workspace = input_folder
# 新建一个output数据库
create_gdb()
# 找到所有dwg文件，并提取信息到数据库
dwg2gdb(point_table, polyline_table, polygon_table, annotation_table)
# 新建aprx工程文件，新建map，数据可视化
data_visualization(output_folder)
