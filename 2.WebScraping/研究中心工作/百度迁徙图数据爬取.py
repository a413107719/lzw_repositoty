from urllib import request
from urllib import error
import re
import xlrd
import xlwt
import threading

def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    style.font = font
    # style.borders = borders
    return style


# 百度地图api城市代码https://www.itsvse.com/thread-3778-1-1.html
# 百度迁徙地图http://qianxi.baidu.com/
if __name__ == '__main__':
    f = xlwt.Workbook()
    sheet2 = f.add_sheet(u'sheet2', cell_overwrite_ok=True)  # 创建sheet2
    row0 = [u'迁入城市',u'所在城市',u'lyd',u'迁出城市',u'所在城市',u'lyd']
     # 生成第一行
    for i in range(0, len(row0)):
        sheet2.write(0, i, row0[i], set_style('Times New Roman', 200, True))

    headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
    opener = request.build_opener()
    opener.add_headers = [headers]
    request.install_opener(opener)

    riqi = input("日期是：")
    # ID = [53,54,315,317,316,348,224,161,346,163,365]
    # name = ["长春","延边","南京","无锡","徐州","常州","苏州","南通","扬州","南昌","赣州"]
    ID = [305]
    name = ["柳州市"]

    for i in range(0,len(ID)):
        firsturl = "http://huiyan.baidu.com/migration/api/cityrank?dt=city&id="+str(ID[i])+"&type=move_in&date="+str(riqi)+"&callback=jsonp"
        data = request.urlopen(firsturl).read().decode("utf-8")
        data = data.encode("utf-8").decode("unicode_escape")
        #对Unicode编码进行改造
        pat = '{"city_name":"(.*?)","province_name":".*?","value":.*?}'
        pat1 = '{"city_name":".*?","province_name":".*?","value":(.*?)}'
        result = re.compile(pat).findall(str(data))
        result1 = re.compile(pat1).findall(str(data))
        column0 = result
        column1 = result1
        column2 = name[i]
        for i1 in range(0, len(column0)):
            sheet2.write(i1 + len(column0)*i+1, 0, column0[i1], set_style('Times New Roman', 220))
        for i1 in range(0, len(column0)):
            sheet2.write(i1 + len(column0)*i+1, 1, column2, set_style('Times New Roman', 220))
        for i1 in range(0, len(column1)):
            sheet2.write(i1 +len(column0)*i+1, 2, column1[i1], set_style('Times New Roman', 220))

    for i in range(0, len(ID)):
        firsturl = "http://huiyan.baidu.com/migration/api/cityrank?dt=city&id="+str(ID[i])+"&type=move_out&date="+str(riqi)+"&callback=jsonp"
        print(firsturl)
        data2 = request.urlopen(firsturl).read().decode("utf-8")
        data2 = data2.encode("utf-8").decode("unicode_escape")  #
        #对Unicode编码进行改造
        pat = '{"city_name":"(.*?)","province_name":".*?","value":.*?}'
        pat1 = '{"city_name":".*?","province_name":".*?","value":(.*?)}'
        result2 = re.compile(pat).findall(str(data2))
        result12 = re.compile(pat1).findall(str(data2))
        column0 = result2
        column1 = result12
        column2 = name[i]
        for i1 in range(0, len(column0)):
            sheet2.write(i1 + len(column0)*i+1, 3, column0[i1], set_style('Times New Roman', 220))
        for i1 in range(0, len(column0)):
            sheet2.write(i1 + len(column0) * i + 1, 4, column2, set_style('Times New Roman', 220))
        for i1 in range(0, len(column1)):
            sheet2.write(i1 + len(column0)*i+1, 5, column1[i1], set_style('Times New Roman', 220))

    print("下载成功！")
    filename = 'D:/shuju/baidumap'+str(riqi)+'.xls'
    f.save(filename)

