# -*- coding=UTF-8 -*-
import arcpy
import csv


def get_polygon_coord(infeature):
    temptfeature = infeature + 'tempt'
    tempttable = infeature + 'tempttable'
    # 将坐标系转为大地坐标系，并计算经纬度
    arcpy.Project_management(in_dataset=infeature, out_dataset=temptfeature,
                             out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",
                             transform_method=[],
                             in_coor_system="PROJCS['CGCS2000_3_Degree_GK_Zone_35',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',35500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',105.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
                             preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")
    arcpy.AddFields_management(in_table=temptfeature, field_description=[["Left", "DOUBLE", "", "", "", ""],
                                                                         ["Bottom", "DOUBLE", "", "", "", ""],
                                                                         ["Right", "DOUBLE", "", "", "", ""],
                                                                         ["Top", "DOUBLE", "", "", "", ""]])
    # 计算矩形四个角点的经纬度
    arcpy.CalculateGeometryAttributes_management(temptfeature, [["Left", "EXTENT_MIN_X"], ["Bottom", "EXTENT_MIN_Y"],
                                                                ["Right", "EXTENT_MAX_X"], ["Top", "EXTENT_MAX_Y"]])
    arcpy.Statistics_analysis(in_table=temptfeature, out_table=tempttable,
                              statistics_fields=[["Left", "MIN"], ["Bottom", "MIN"], ["Right", "MAX"], ["Top", "MAX"]],
                              case_field=[])
    cursor = arcpy.SearchCursor(tempttable)
    original_coord = []
    for row in cursor:
        leftmin = row.MIN_Left
        rightmax = row.MAX_Right
        bottommin = row.MIN_Bottom
        topmax = row.MAX_Top
        original_coord = [leftmin, topmax, rightmax, bottommin]
    return original_coord


def resize(coord_list):
    newcoord_list = []
    while coord_list:
        for coord in coord_list:
            Q, R, S, T = coord[0], coord[1], coord[2], coord[3]
            x = S - Q
            y = R - T
            if x > y and x / y > 2:
                list = [[Q, R, (Q+S)/2, T], [(Q+S)/2, R, S, T]]
                coord_list += list
            elif x < y and y / x > 2 :
                list = [[Q, R, S, (R + T)/2], [Q, (R + T)/2, S, T]]
                coord_list += list
            else:
                newcoord_list.append(coord)
            coord_list.remove(coord)
            # print(coord, coord_list,'new:', newcoord_list,sep='______')
    return newcoord_list


def cut_polygon_mutiple(coordlist, cut_times):
    i = 0
    result = []
    while i < cut_times:
        if result != []:
            coordlist = result
            result=[]
        for coord in coordlist:
            a, b, c, d = coord[0], coord[1], coord[2], coord[3]
            cutlist = [[a, b, (a+c)/2, (b+d)/2], [(a+c)/2, (b+d)/2, c, d], [(a+c)/2, b, c, (b+d)/2], [a, (b+d)/2, (a+c)/2, d]]
            result += cutlist
        i += 1
    return result


def cutpolygon_with_polygon(xianyu, xiancheng):
    G, J, I, H = xianyu[0], xianyu[1], xianyu[2], xianyu[3]
    g, j, i, h = xiancheng[0], xiancheng[1], xiancheng[2], xiancheng[3]
    coordlist = [[G, J, g, j], [g, J, i, j], [i, J, I, j], [i, j, I, h], [i, h, I, H], [g, h, i, H], [G, h, g, H], [G, j, g, h], xiancheng]
    resized_coordlist = resize(coordlist)
    cut_coordlist = cut_polygon_mutiple(resized_coordlist, 2)
    return cut_coordlist
    # gaode_coordlist, csv_coordlist = build_gaodeandcsv_coord(cut_coordlist)
    # writeinto_csv(csvpath, ("num", "coord"), csv_coordlist)


def build_gaodeandcsv_coord(coordlist):
    gaodecoordlist = []
    csvcoordlist = []
    for coord in coordlist:
        gaode_coord = str(coord[0]) + ',' + str(coord[1]) + '|' + str(coord[2]) + ',' + str(coord[3])
        gaodecoordlist.append(gaode_coord)

        csv_coord = [str(coord[0]) + ',' + str(coord[1]), str(coord[2]) + ',' + str(coord[3])]
        # csvcoordlist.append(csv_coord)
        csvcoordlist += csv_coord
    return gaodecoordlist, csvcoordlist


# 新建csv并写入值
def writeinto_csv(path, field_names, data_rows):
    csvFile = open(path, 'w', newline='')      # 1. 创建文件对象
    csv_writer = csv.writer(csvFile)      # 2. 基于文件对象构建 csv写入对象
    csv_writer.writerow(field_names)      # 3. 构建列表头
    number = 1
    for row in data_rows:
        data_row = [number, row]
        csv_writer.writerow(data_row)      # 4. 写入csv文件内容
        number += 1
    csvFile.close()     # 5. 关闭文件


if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    xianyu_polygon = r'F:\测试数据\高德api爬取\New File Geodatabase.gdb\CJDCQ'
    # xiancheng_polygon = r'F:\测试数据\高德api爬取\New File Geodatabase.gdb\xiancheng'
    xiancheng_polygon = ''
    csvpath = "F:/test17.csv"

    # 提取县域范围坐标
    xianyu_coord = get_polygon_coord(xianyu_polygon)
    # 存在县城范围，则提取县城范围坐标
    if xiancheng_polygon != '':
        arcpy.AddMessage('xiancheng exist')
        xiancheng_coord = get_polygon_coord(xiancheng_polygon)
        coord_list = cutpolygon_with_polygon(xianyu_coord, xiancheng_coord)

    # 如果不存在，则直接切4刀
    else:
        arcpy.AddMessage('xiancheng does not exist')
        coord_list = cut_polygon_mutiple([xianyu_coord], 4)

    # 新建csv并写入值
    gaode_coordlist, csv_coordlist = build_gaodeandcsv_coord(coord_list)
    writeinto_csv(csvpath,("num", "coord"), csv_coordlist)
    print(len(coord_list), coord_list)


