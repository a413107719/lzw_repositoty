# -*- coding=UTF-8 -*-
import arcpy
import pandas as pd

arcpy.env.overwriteOutput = True
infeature = r'F:\测试数据\高德api爬取\New File Geodatabase.gdb\CJDCQ'
temptfeature = infeature + 'tempt'
tempttable = infeature + 'tempttable'

arcpy.Project_management(in_dataset=infeature, out_dataset=temptfeature,
                         out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", transform_method=[], in_coor_system="PROJCS['CGCS2000_3_Degree_GK_Zone_35',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',35500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',105.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
arcpy.AddFields_management(in_table=temptfeature, field_description=[["Left", "DOUBLE", "", "", "", ""], ["Bottom", "DOUBLE", "", "", "", ""], ["Right", "DOUBLE", "", "", "", ""], ["Top", "DOUBLE", "", "", "", ""]])
arcpy.CalculateGeometryAttributes_management(temptfeature, [["Left", "EXTENT_MIN_X"], ["Bottom", "EXTENT_MIN_Y"], ["Right", "EXTENT_MAX_X"], ["Top", "EXTENT_MAX_Y"]])
arcpy.Statistics_analysis(in_table=temptfeature, out_table=tempttable, statistics_fields=[["Left", "MIN"], ["Bottom", "MIN"], ["Right", "MAX"], ["Top", "MAX"]], case_field=[])

cursor = arcpy.SearchCursor(tempttable)

for row in cursor:
    leftmin = row.MIN_Left
    rightmax = row.MAX_Right
    bottommin = row.MIN_Bottom
    topmax = row.MAX_Top
    print(leftmin, rightmax, bottommin, topmax, sep='  ')
    polygon = str(leftmin) + ',' + str(topmax) + '|' + str(rightmax) + ',' + str(bottommin)
print(polygon)


