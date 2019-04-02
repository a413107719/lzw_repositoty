from TB_func import pack_imformation
import time
from TB_channerl_extract import kinds_data
# from multiprocessing import Pool   # P是大写

host_url = 'http://poi.mapbar.com/zigong/'
urlANDname_list = kinds_data(host_url)
for i in urlANDname_list:
    pack_imformation(i)
    time.sleep(3)

# 正确的多进程访问代码，但因网站的反爬限制，无法使用。可在其它网站上套用
# if __name__ == "__main__":
#     pool = Pool()  # 创建进程池
#     host_url = 'http://poi.mapbar.com/zigong/'
#     urlANDname_list = kinds_data(host_url)
#     pool.map(pack_imformation, urlANDname_list)
