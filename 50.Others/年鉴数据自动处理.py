import openpyxl
import os


def get_sheet_name(excel):
    workbook = openpyxl.load_workbook(excel)
    sheet = workbook['Sheet1']
    # todo: 提取表名
    sheet_name = 'aaa'
    return sheet,sheet_name

def get_column_names(sheet):
    pass

def get_sheet_value():
    pass


input_path = 'E:\\02研究中心工作\\12.处理Excel多级表头\\重庆统计年鉴2018（光盘版）\\重庆统计年鉴2018\\zk\\html'
# 获取所有年鉴excel表格
os.chdir(input_path)
excels = []

for excel in excels:
    # 每个excel提取标题
    sheet, sheet_name = get_sheet_name(excel)
    # 每个excel合并、提取表头
    get_column_names(sheet)
    # 每个excel提取数据内容
    get_sheet_value()
    # 在输入文件夹中新建一个excel表，以标题命名，表头在第一行，数据内容在其后













# os.chdir('E:\\02研究中心工作\\12.处理Excel多级表头')
# wb = openpyxl.load_workbook('年鉴表头样式.xls')
# sheet = wb['Sheet1']         # 选择一个excel页面