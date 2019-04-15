from collections import OrderedDict
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from prettytable import PrettyTable
import matplotlib.pyplot as plt


# 不同max_features取值对应误差大小
def findbest_maxfeatures():
    # 据此修改https://scikit-learn.org/dev/auto_examples/ensemble/plot_ensemble_oob.html#sphx-glr-auto-examples-ensemble-plot-ensemble-oob-py
    RANDOM_STATE = 123
    ensemble_clfs = []
    x_columns = traindata_all.columns[1:len(traindata_all.columns) - 1]
    for i in range(len(x_columns)):
        ensemble_clfs.append((i + 1, RandomForestClassifier(n_estimators=20, warm_start=True, oob_score=True,
                                                            max_features=i + 1, random_state=RANDOM_STATE)))
    error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)
    print(error_rate)
    print('-----')
    # print(ensemble_clfs)

    # 绘制表格
    print('-- 不同max_features取值对应误差大小 --')
    table3 = PrettyTable(['随机特征个数', '误差率'])
    for label, clf in ensemble_clfs:
        clf.fit(X, y)
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((round(oob_error, 4)))
        table3.add_row([label, round(oob_error, 4)])
    print(table3)
    # print(error_rate)

# 获取数据
traindata_all = pd.read_csv("D:/data24.csv")
traindata_all.columns = ["ID", "TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP", "SLP", "SI"]
# 将数据集分为训练集和测试集
X, y = traindata_all.iloc[:, 1:len(traindata_all.columns) - 1].values, traindata_all.iloc[:, len(traindata_all.columns) - 1].values     # 选择评价特征和标签特征
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
findbest_maxfeatures()

