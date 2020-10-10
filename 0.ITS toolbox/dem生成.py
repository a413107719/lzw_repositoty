# -*- coding: utf-8 -*-
import arcpy
"""
此脚本的优势是能够解决用gispro或arcmap不能对县域大量等高线和高程点数据进行处理的问题
"""

# 输入参数
dgx = "I:\\毕节国土空间规划\\分析库\\地形图信息提取.gdb\\等高线_首曲线"
gcd = "I:\\毕节国土空间规划\\分析库\\地形图信息提取.gdb\\高程点"
# 输出参数
cellsize = "5"  # 以米为单位
tin = "F:\\test\\tin"
dem = "F:\\test\\dem"


arcpy.env.overwriteOutput = True
arcpy.AddMessage("begin to create TIN.....")
arcpy.CreateTin_3d(out_tin=tin, spatial_reference="", in_features=[[dgx, "Elevation", "Hard_Line", "<None>"], [gcd, "Elevation", "Mass_Points", "<None>"]], constrained_delaunay="DELAUNAY")
arcpy.AddMessage("begin to create DEM.....")
arcpy.TinRaster_3d(in_tin=tin, out_raster=dem, data_type="FLOAT", method="LINEAR", sample_distance="CELLSIZE " + cellsize, z_factor=1, sample_value=250)

