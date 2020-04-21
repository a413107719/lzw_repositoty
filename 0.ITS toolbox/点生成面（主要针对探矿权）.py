import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 2000)

# excel = "F:\\测试数据\\酉阳\\cxy探矿权处理\\酉阳县矿山采矿权信息统计表.xlsx"
excel = "F:\\测试数据\\酉阳\\cxy探矿权处理\\酉阳县探矿权信息统计表.xlsx"
df = pd.read_excel(excel, header=1)
# print(df['坐标'].str.split(','))
df['坐标1'] = 0
print(df.head(5))


for i in range(len(df)):
    # print(i+1)
    # value = df.loc[i][2]
    value = df.loc[i][3]
    if value[-1] != ',':
        value = value + ','
    value = value.replace(',,', ',')
    value = value.replace('，', ',')
    value = value.replace('\n', '')
    text = str(value).split(',')
    # print(text)
    valuelist = text[2: -4]
    # print(valuelist)
    pointlist = []
    x = 0
    while x < len(valuelist):
        pointlist.append(valuelist[x+1] + '#' + valuelist[x+2])
        x += 3
    # print(pointlist)
    df.loc[i, '坐标1'] = str(pointlist).replace('[', '').replace('\'', '').replace(']', '')

del df['坐标']
df2 = df.drop('坐标1', axis=1).join(df['坐标1'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('坐标2'))
# print(df2)
df2['经度'], df2['纬度'] = df2['坐标2'].str.split('#', 1).str
del df2['坐标2']
print(df2)

outputroute = 'F:\\测试数据\\酉阳\\cxy探矿权处理\\test.xls'
writer = pd.ExcelWriter(outputroute)
df2.to_excel(writer, float_format='%.5f')
writer.save()

