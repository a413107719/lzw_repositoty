import os,time
#获取命令行输入的关机时间
input_time = str(input("请输入关机时间："))
#转换成时间戳
time1 = time.strptime(input_time,"%Y-%m-%d %H:%M:%S")
time2 = int(time.mktime(time1))
#获取当前系统时间时间戳
now = int(time.time())
#计算电脑关机的等待时间
d = time2 - now
print("距关机还有%d秒" %d)
os.system('shutdown -s -t %d' %d)