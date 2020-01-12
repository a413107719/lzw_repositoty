import pandas as pd
import random
from retrying import retry

@retry(stop_max_attempt_number=3)
def mainfunction():
    dic = dics.copy()
    try:
        for date in dates:
            list = random.sample(dic.keys(), 3)
            df.loc[date] = list
            for y in list:
                dic[y] -= 1
                if dic[y] == 0:
                    del dic[y]
            # break
        print('success')
    except Exception as e:
        print('fail,try again')
        mainfunction()


dics = {'刘进': 6, '高成凯': 6, '王德平': 6, '杨果': 6, '邓丹': 6, '何佳': 6}
dates = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
columnname = ['值班人1', '值班人2', '值班人3']

# pd.set_option('display.max_colwidth', 20)
df = pd.DataFrame(index=dates, columns=columnname)
datadf = mainfunction()

print()
print(df)






