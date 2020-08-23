import pandas as pd


def gets_kindcodelist(excel, sheetname):
    column = 'NEW_TYPE'
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(excel, sheet_name=sheetname, converters={column: str})
    df['type'] = df[column]
    df[['type']] = df[['type']].apply(pd.to_numeric)
    dfselect = df[df['type'] % 10000 == 0]
    print('小类行列数:', dfselect.shape)
    codelist = dfselect[column].tolist()
    return codelist


if __name__ == '__main__':
    # 参数
    excel = r'F:\高德poi爬取\amap_poicode.xlsx'
    sheetname = 'POI分类与编码'

    # 执行程序
    kindlist = gets_kindcodelist(excel, sheetname)
    print(kindlist)
