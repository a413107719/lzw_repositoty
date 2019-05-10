from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix as con
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
from collections import OrderedDict
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from prettytable import PrettyTable
from sklearn.model_selection import cross_val_score

from sklearn.neighbors import KNeighborsClassifier  #一个简单的模型，只有K一个参数，类似K-means
from pylab import mpl



# 获取数据
traindata_all = pd.read_csv("D:/data24.csv")
traindata_all.columns = ["ID", "TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP",
                         "SLP", "SI"]

# 将数据集分为训练集和测试集
X, y = traindata_all.iloc[:, 1:len(traindata_all.columns) - 1].values, traindata_all.iloc[:, len(traindata_all.columns) - 1].values  # 选择评价特征和标签特征
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


def cross_validation():
    k_range = range(1, 31)
    cv_scores = []		# 用来放每个模型的结果值
    for n in k_range:
        knn = KNeighborsClassifier(n)   # knn模型，这里一个超参数可以做预测，当多个超参数时需要使用另一种方法GridSearchCV
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')  # cv：选择每次测试折数  accuracy：评价指标是准确度,可以省略使用默认值
        cv_scores.append(scores.mean())
    max_score = max(cv_scores)
    max_index = cv_scores.index(max_score)

    # 绘出图形
    plt.plot(k_range, cv_scores)
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.title("交叉验证", fontsize=18)
    plt.xlabel('K_range')
    plt.ylabel('Accuracy')		# 通过图像选择最好的参数
    plt.show()
    best_knn = KNeighborsClassifier(n_neighbors=max_index)	 # 选择最优的K=3传入模型
    best_knn.fit(X_train, y_train)			# 训练模型
    print('------ 交叉验证 ------')
    table4 = PrettyTable(['最优K值', '最优评分'])
    table4.add_row([max_index, round(best_knn.score(X_test, y_test), 4)])
    print(table4)
    print()

cross_validation()