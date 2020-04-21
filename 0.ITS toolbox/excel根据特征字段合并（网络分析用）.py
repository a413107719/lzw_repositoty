import geohash
import pandas as pd


infid = "IN_FID"
nearfc = "NEAR_FC"
nearfid = 'NEAR_FID'
poi = "轨道公交"
mid = "社区质心"

# 构建结果dataframe
outputdataframe = pd.DataFrame(columns=(infid, poi, mid))


excelfile = 'F:\\测试数据\\网络拆数据\\P社区交通.xls'
data = pd.read_excel(excelfile)
unique_infid = data[infid].unique()

for value in unique_infid:
    # value = 610
    sub_df = data [data[infid].isin([value])]
    sub_df_point = sub_df[sub_df[nearfc].isin([poi])]
    sub_df_mid = sub_df[sub_df[nearfc].isin([mid])]
    datalist = value, list(sub_df_point[nearfid]), list(sub_df_mid[nearfid])
    print(value, list(sub_df_point[nearfid]), list(sub_df_mid[nearfid]))

    dic = [{infid: value, poi: str(list(sub_df_point[nearfid])).split('[')[1].split(']')[0], mid: str(list(sub_df_mid[nearfid])).split('[')[1].split(']')[0]}]
    # print(dic)
    # print()
    outputdataframe = outputdataframe.append(dic, ignore_index=True)
    # break

# print(outputdataframe)
# print(outputdataframe[poi])

outputdataframe1 = outputdataframe.drop(poi, axis=1).join(outputdataframe[poi].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename(poi))
print(outputdataframe1)

outputroute = excelfile.split('.')[0] + 'output' + '.xls'
writer = pd.ExcelWriter(outputroute)
outputdataframe1.to_excel(writer, float_format='%.5f')
writer.save()
