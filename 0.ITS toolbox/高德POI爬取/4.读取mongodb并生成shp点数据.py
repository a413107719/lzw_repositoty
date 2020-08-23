import pymongo
import pandas as pd

'''根据mongodb数据库中的经纬度直接生成shp还未做，导致每次都得通过fme，最好使用geopandas来做，有空再折腾吧。。。'''

# 设置df打印格式，可删除
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth',  30)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 读取mongodb
client = pymongo.MongoClient('localhost',27017)
db = client['zkStudio']
pk10 = db['yiliang_poi_final']
df = pd.DataFrame(list(pk10.find()))

# 拆分经纬度
df['longitude'], df['lattitude'] = df['location'].str.split(',', 1).str
df[['longitude', 'lattitude']] = df[['longitude', 'lattitude']].apply(pd.to_numeric)
print(df)

# 根据经纬度转成点数据
import arcpy

