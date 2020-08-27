import arcpy


gdbpath = r'F:\test\new.gdb'

arcpy.env.workspace = gdbpath
tables = arcpy.ListTables()
features = arcpy.ListFeatureClasses()
for y in [tables, features]:
    print('\n', y)
    for i in y:
        rowcount = arcpy.GetCount_management(i)
        if int(str(rowcount)) == 0:
            arcpy.Delete_management(gdbpath + '\\' + i)  # 在GDB中删除数据
            print(i + "： 由于数据为空，已在GDB中删除")




