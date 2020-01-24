import arcpy
import pandas as pd
import shutil

# 使用时仅需修改此处内容,注意目录分隔是\\
mainpath = "F:\\测试数据\\地理国情处理\\"
original_gdbname = '500242.gdb'
excel = 'F:\\测试数据\\地理国情处理\\基础地理国情解译表\\基础性地理国情监测名称表test.xlsx'


# 获取要素类对应表
excel_df = pd.read_excel(excel)
excel_gr = excel_df.groupby(by=['数据集名称', '数据集代码']).size()  # 得到featuredataset转译表
# print(excel_featruedataset)
muban_featuredatasetcode_list, muban_featuredatasetname_list = [], []
for index in excel_gr.index:
    muban_featuredatasetcode_list.append(index[1])
    muban_featuredatasetname_list.append(index[0])
print('模板要素类包括：', muban_featuredatasetcode_list, muban_featuredatasetname_list)


# 复制原始gdb，新建临时gdb
out_gdbname = 'output' + original_gdbname
origianlgdb_path = mainpath + original_gdbname
outputgdbpath = mainpath + out_gdbname
if arcpy.Exists(outputgdbpath):
    shutil.rmtree(outputgdbpath)
print('正在复制gdb')
shutil.copytree(origianlgdb_path, outputgdbpath)

# 开始处理
arcpy.env.workspace = outputgdbpath
featuredatasets_list = arcpy.ListDatasets()
print('gdb包含要素类：', featuredatasets_list)    # gdb包含要素类  ['LcrDataset', 'StrDataset', 'TraDataset']
for dataset in featuredatasets_list:
    if dataset in muban_featuredatasetcode_list:
        featurelist = arcpy.ListFeatureClasses(feature_dataset=dataset)
        print('\n', "开始处理要素类：", dataset, '包括要素：', featurelist)
        for featurecode in featurelist:
            select = excel_df.loc[excel_df['数据代码'] == featurecode]
            if select.empty is not True:
                featurename = select.iloc[0, 2]
                # 修改要素名称
                print('正在修改要素：', featurename, featurecode)
                arcpy.Rename_management(featurecode,featurename)
        # 修改要素类名称
        featuredataset_code = dataset
        featuredataset_name = muban_featuredatasetname_list[muban_featuredatasetcode_list.index(dataset)]
        print('正在修改要素类：', featuredataset_name, featuredataset_code)
        arcpy.Rename_management(featuredataset_code,featuredataset_name)
print("清洗完成！！！")





