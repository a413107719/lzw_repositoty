import os
import time
from shutil import copy2
import shutil


# 根据传参判断复制的目标地址是否存在如果不存在进行创建，并且执行复制操作
def copy_file(src_file, dst_dir):
    if os.path.isdir(dst_dir):
        pass
    else:
        os.makedirs(dst_dir)
    copy2(src_file, dst_dir)


# 遍历整个图片路径底下的所有文件并获取其创建时间，根据创建时间进行复制操作
def walk_file(file_path):
    for root, dirs, files in os.walk(file_path, topdown=False):
        # root所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs是一个list ，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files同样是list, 内容是该文件夹中所有的文件(不包括子目录)
        for name in files:
            # 构造每个文件的原始路径
            com_name = os.path.join(root, name)
            # 获取文件的修改时间
            t = os.path.getmtime(com_name)
            real_year = time.localtime(t).tm_year
            real_mon = time.localtime(t).tm_mon
            real_day = time.localtime(t).tm_mday
            # print(str(real_year) + str(real_mon) + str(real_day) + name)
            # 复制文件
            copy_path_str = CopyPath + "\\" + str(real_year) + r"-" + str(real_mon) + r"-" + str(real_day)
            copy_file(com_name, copy_path_str)
        # 处理子文件夹数据
        for subfolder in dirs:
            walk_file(subfolder)

def find_singlephoto():
    other_folder = CopyPath + '\\' + '其它'
    # os.makedirs(other_folder)
    for root, dirs, files in os.walk(CopyPath, topdown=False):
        for folder in dirs:
            # folder_path = os.path.join(CopyPath , '' , folder)
            folder_path = CopyPath+'\\'+folder
            file_num = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
            # print(folder + ':' + str(file_num))
            if file_num < 2:
                if os.path.isdir(other_folder):
                    pass
                else:
                    os.makedirs(other_folder)
                for root1 ,dirs1, files1 in os.walk(folder_path,topdown=False):
                    # print(files1)
                    for file in files1:
                        file_path1 = folder_path + '\\' + file
                        print(file_path1)
                        copy2(file_path1, other_folder)
                    print('已经删除目录'+ folder_path)
                    shutil.rmtree(folder_path)


# 图片所处的绝对路径，其中r表示去掉python的内部转义
PicPath = r'F:\照片整理'
CopyPath = r'F:\photozhengli'
walk_file(PicPath)
find_singlephoto()
