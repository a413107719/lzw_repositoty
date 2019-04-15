import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
 
train_data = pd.read_csv("D:/data2.csv")
 



predictors = ["TR","TCH","FZZ","MZ","SLH","TRJ","TRS","SJD","JMD","DM","PW","ELE","ASP","SLP"]
results = []
sample_leaf_options = list(range(1, 500, 3))
n_estimators_options = list(range(1, 1000, 5))
groud_truth = train_data['SI'][601:]
print("sss")
for leaf_size in sample_leaf_options:
    for n_estimators_size in n_estimators_options:
        alg = RandomForestClassifier(min_samples_leaf=leaf_size, n_estimators=n_estimators_size, random_state=50)
        alg.fit(train_data[predictors][:600], train_data['SI'][:600])
        predict = alg.predict(train_data[predictors][601:])
        # 用一个三元组，分别记录当前的 min_samples_leaf，n_estimators， 和在测试数据集上的精度
        results.append((leaf_size, n_estimators_size, (groud_truth == predict).mean()))
        # 真实结果和预测结果进行比较，计算准确率
        print((groud_truth == predict).mean())

# 打印精度最大的那一个三元组
print("End".max(results, key=lambda x: x[2]))
print("End")