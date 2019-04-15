import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix as con
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import prettytable
from prettytable import PrettyTable



# 因子重要性判断
def top_variable_importance():
    # 对训练好的随机森林，完成重要性评估
    importances = forest.feature_importances_
    # print(importances)
    x_columns = traindata_all.columns[1:len(traindata_all.columns)-1]
    indices = np.argsort(importances)[::-1]
    # print(indices)
    np.argsort(x_columns,)
    list=[]
    print('---------- Top Variable Importance ----------')
    for f in range(X_train.shape[1]):
        # 对于最后需要逆序排序，我认为是做了类似决策树回溯的取值，从叶子收敛
        # 到根，根部重要程度高于叶子。
        print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))
        list.append(feat_labels[indices[f]])
    # print(list)
    # 筛选变量（选择重要性比较高的变量）
    threshold = 0.15
    x_selected = X_train[:, importances > threshold]

    # 可视化
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.title("数据集中各个特征的重要程度", fontsize=18)
    plt.ylabel("import level", fontsize=15, rotation=90)
    plt.rcParams['font.sans-serif'] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False
    for i in range(x_columns.shape[0]):
        plt.bar(i, importances[indices[i]], color='orange', align='center')
        plt.xticks(np.arange(x_columns.shape[0]), list, rotation=90, fontsize=12)
    plt.show()

# 分类树数量和误差率的关系
def findbest_n_estimators(max_trees_num):
    learning_rate = 1

    dt_stump = DecisionTreeClassifier(max_depth=1, min_samples_leaf=1)
    dt_stump.fit(X_train, y_train)
    dt_stump_err = 1.0 - dt_stump.score(X_test, y_test)

    dt = DecisionTreeClassifier(max_depth=9, min_samples_leaf=1)
    dt.fit(X_train, y_train)
    dt_err = 1.0 - dt.score(X_test, y_test)

    ada_discrete = AdaBoostClassifier(
        base_estimator=dt_stump,
        learning_rate=learning_rate,
        n_estimators=max_trees_num,
        algorithm="SAMME")
    ada_discrete.fit(X_train, y_train)

    ada_real = AdaBoostClassifier(
        base_estimator=dt_stump,
        learning_rate=learning_rate,
        n_estimators=max_trees_num,
        algorithm="SAMME.R")
    ada_real.fit(X_train, y_train)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot([1, max_trees_num], [dt_stump_err] * 2, 'k-',
            label='Decision Stump Error')
    ax.plot([1, max_trees_num], [dt_err] * 2, 'k--',
            label='Decision Tree Error')

    ada_discrete_err = np.zeros((max_trees_num,))
    for i, y_pred in enumerate(ada_discrete.staged_predict(X_test)):
        ada_discrete_err[i] = zero_one_loss(y_pred, y_test)

    ada_discrete_err_train = np.zeros((max_trees_num,))
    for i, y_pred in enumerate(ada_discrete.staged_predict(X_train)):
        ada_discrete_err_train[i] = zero_one_loss(y_pred, y_train)

    ada_real_err = np.zeros((max_trees_num,))
    for i, y_pred in enumerate(ada_real.staged_predict(X_test)):
        ada_real_err[i] = zero_one_loss(y_pred, y_test)

    ada_real_err_train = np.zeros((max_trees_num,))
    for i, y_pred in enumerate(ada_real.staged_predict(X_train)):
        ada_real_err_train[i] = zero_one_loss(y_pred, y_train)

    ax.plot(np.arange(max_trees_num) + 1, ada_discrete_err,
            label='Discrete AdaBoost Test Error',
            color='red')
    ax.plot(np.arange(max_trees_num) + 1, ada_discrete_err_train,
            label='Discrete AdaBoost Train Error',
            color='blue')
    ax.plot(np.arange(max_trees_num) + 1, ada_real_err,
            label='Real AdaBoost Test Error',
            color='orange')
    ax.plot(np.arange(max_trees_num) + 1, ada_real_err_train,
            label='Real AdaBoost Train Error',
            color='green')

    ax.set_ylim((0.0, 0.5))
    ax.set_xlabel('max_trees_num')
    ax.set_ylabel('error rate')

    leg = ax.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.7)

    plt.show()


if __name__ == '__main__':
    # 获取数据
    traindata_all = pd.read_csv("D:/data24.csv")
    traindata_all.columns = ["ID", "TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP", "SLP", "SI"]

    # 将数据集分为训练集和测试集
    X, y = traindata_all.iloc[:, 1:len(traindata_all.columns) - 1].values, traindata_all.iloc[:, len(traindata_all.columns) - 1].values     # 选择评价特征和标签特征
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 打印评价特征和标签特征
    feat_labels = traindata_all.columns[1:len(traindata_all.columns)-1]
    print('\n' + '--- Data summary ---')
    # info_url = traindata_all.info()
    print('评价特征名称为：'+str([x for x in feat_labels]) )
    print('标签特征名称为：' + str(traindata_all.columns[len(traindata_all.columns)-1])+'\n')
    print('--- 标签特征统计表 ---')
    yValue_table = traindata_all['SI'].value_counts()
    table2 = PrettyTable(['值', '数量', '占比'])
    for i in range(len(yValue_table)):
        value = yValue_table.index[i]
        number = yValue_table[value]
        table2.add_row([value, number, round(number/len(X), 2)])
    print(table2)
    print()


    # 建立模型
    forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)  # 实例化
    forest.fit(X_train, y_train)   # 用训练集数据训练模型
    result = forest.fit(X_train, y_train).predict(X_test)
    # 打印混淆矩阵
    print('------------ 随机森林模型混淆矩阵 ------------')
    table = con(y_test, result)
    table_x = PrettyTable(['实际类别', '预测适宜', '预测不适宜', '分类误差率'])
    table_x.add_row(["适宜", table[0][0], table[0][1], round(table[0][1] / table[0][0], 2)])
    table_x.add_row(["不适宜", table[1][0], table[1][1], round(table[1][1] / table[1][0], 2)])
    print(table_x)
    score = forest.score(X_test, y_test)    # 测试准确率
    print('准确率： ' + str(round(score, 2)) + '\n')

    # 分类树数量和误差率的关系
    findbest_n_estimators(100)

    # 因子重要性判断
    top_variable_importance()
