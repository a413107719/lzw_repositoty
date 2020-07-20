import pandas as pd
import arcpy

# excel参数
tablepath = arcpy.GetParameterAsText(0)  # "Z:\\0.Cloudstation\\02.工作\\23.旅游资源分类转译\\旅游资源分类转译表.xlsx"
codename = arcpy.GetParameterAsText(1)  # '基本类型'
realname = arcpy.GetParameterAsText(2)  # '基本类型转译'

# shp数据参数
shp_path = arcpy.GetParameterAsText(3)  # "Z:\\0.Cloudstation\\02.工作\\23.旅游资源分类转译\\New File Geodatabase.gdb\\旅游资源普查"
shp_codename = arcpy.GetParameterAsText(4)  # '基本类型'
shp_realname = arcpy.GetParameterAsText(5)  # '基本类型转译'

arcpy.AddMessage(tablepath)
arcpy.AddMessage(codename)
arcpy.AddMessage(realname)
arcpy.AddMessage(shp_path)
arcpy.AddMessage(shp_codename)
arcpy.AddMessage(shp_realname)


# 构建转译表
df = pd.read_excel(tablepath)
df2 = df.fillna(method='pad')  # 数据向下补全
df3 = df2.groupby([codename, realname]).count()
df4 = df3.index.to_frame()
df5 = df4.replace(' ', '', regex=True, inplace=True)  # 替换数据框中的空值
print(df4.head(10))

# 开始转译
arcpy.env.overwriteOutput = True
arcpy.AddField_management(shp_path, shp_realname, field_type='text')
# 循环给字段赋值
cursor = arcpy.UpdateCursor(shp_path)
for row in cursor:
    codevalue = row.getValue(codename)
    dfselect = df4[df4[codename] == codevalue]   # 取得某一字段值等于codevalue的行
    if dfselect.empty != True:
        selectvalue = dfselect[realname][0]   # 取得某一字段第一个值
        print(codevalue, selectvalue)
        row.setValue(shp_realname, selectvalue)
        cursor.updateRow(row)
    else:
        arcpy.AddMessage('错误值%s' % (codevalue))

