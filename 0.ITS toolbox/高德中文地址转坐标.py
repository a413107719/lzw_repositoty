import requests

'''地址识别经度不够，待优化'''

def findXY(city, address):
    key = "5b6cc66ab2e8a5c0fb5ee4a2d7c0a564"
    # address = "新都区疾控中心①站"

    try:
        url = "https://restapi.amap.com/v3/geocode/geo?key=" + key + "&address=" + address + "&city=" + city
        response = requests.get(url)
        answer = response.json()
        GPS = answer['geocodes'][0]['location'].split(",")
        longitude, lattitude = GPS[0], GPS[1]
        level = answer['geocodes'][0]['level']
        # print(longitude, lattitude, level, sep='  ')
    except Exception as e:
        longitude, lattitude, level = 0, 0, 0
    return longitude, lattitude, level



# city = "成都市"
# text ='''锦门小学站、毗河苑社区站、观澜鹭岛站、区疾控中心①站、区人民医院站、汇景花园站、区政务服务中心站、香城小学站、
# 东骏湖景湾南门站、兴乐南路站、水沐天城站、缤纷时代广场站、兴乐北路站、成都医学院站、派都广场站、桂林小学站、医学院小区站、
# 福缘小区站、西南石油大学北门站、新都一中站、思学园站、蜀龙大道北段站、地铁钟楼站、钟楼站、桂湖东路站、桂湖中路站、新中路站、
# 小北街站、成医附院站、新新街站、区交通运输局站、现代制造职校站、五里村一组站、五里村八组站、五里村站'''
# text = text.replace('\n', '')
# text = text.replace('站', '公交站')
# addresslist = text.split('、')
# addresslist = ["新都区"+ i for i in addresslist]
# print(addresslist)
#
# findXY(addresslist)
