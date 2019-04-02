import arcpy

pro_aprx = arcpy.mp.ArcGISProject("F:\\测试数据\\地形图信息提取\\地形图信息提取20190118_1117.aprx")
add_data_map = pro_aprx.listMaps("Map")[0]
DGX = add_data_map.listLayers()[3]
print(DGX.name)


