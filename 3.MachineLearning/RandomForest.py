from sklearn.metrics import confusion_matrix as con
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
from collections import OrderedDict
from sklearn.ensemble import RandomForestClassifier
from prettytable import PrettyTable
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier  #一个简单的模型，只有K一个参数，类似K-means
from pylab import mpl
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pydotplus
from sklearn import tree
from IPython.display import Image
import os


# 打印评价特征和标签特征
def print_featurelable():
    feat_labels = traindata_all.columns[1:len(traindata_all.columns) - 1]
    print('\n' + '--- Data summary ---')
    # info_url = traindata_all.info()
    print('评价特征名称为：' + str([x for x in feat_labels]))
    print('标签特征名称为：' + str(traindata_all.columns[len(traindata_all.columns) - 1]) + '\n')
    print('--- 标签特征统计表 ---')
    yvalue_table = traindata_all['SI'].value_counts()
    table2 = PrettyTable(['值', '数量', '占比'])
    for i in range(len(yvalue_table)):
        value = yvalue_table.index[i]
        number = yvalue_table[value]
        table2.add_row([value, number, round(number / len(X), 2)])
    print(table2)
    print()


# 交叉验证
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

# 因子重要性判断
def top_variable_importance(forest):
    feat_labels = traindata_all.columns[1:len(traindata_all.columns) - 1]
    # 对训练好的随机森林，完成重要性评估
    importances = forest.feature_importances_
    # print(importances)
    x_columns = traindata_all.columns[1:len(traindata_all.columns)-1]
    indices = np.argsort(importances)[::-1]
    # print(indices)
    np.argsort(x_columns,)
    list = []
    print('-- 所有变量影响程度排序 --')
    table3 = PrettyTable(['序号', '评价特征', '重要性(%)'])
    for f in range(X_train.shape[1]):
        table3.add_row([f+1, feat_labels[indices[f]], round(importances[indices[f]]*100, 2)])
        list.append(feat_labels[indices[f]])
    print(table3)
    print()
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


# 建立模型
def build_model():
    forest = RandomForestClassifier(n_estimators=500, random_state=0, n_jobs=-1)  # 实例化
    forest.fit(X_train, y_train)  # 用训练集数据训练模型
    result = forest.fit(X_train, y_train).predict(X_test)
    return forest, result


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
    ax.set_xlabel('n_estimators')
    ax.set_ylabel('error rate')

    leg = ax.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.7)

    plt.show()


# 不同max_features取值对应误差大小
def findbest_maxfeatures():
    # 据此修改https://scikit-learn.org/dev/auto_examples/ensemble/plot_ensemble_oob.html#sphx-glr-auto-examples-ensemble-plot-ensemble-oob-py
    RANDOM_STATE = 123
    ensemble_clfs = []
    x_columns = traindata_all.columns[1:len(traindata_all.columns) - 1]
    for i in range(len(x_columns)):
        ensemble_clfs.append((i + 1,
                              RandomForestClassifier(n_estimators=300,
                                                     warm_start=True, oob_score=True,
                                                     max_features=i + 1,
                                                     random_state=RANDOM_STATE)))

    error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)

    print('-- 不同max_features取值对应误差大小 --')
    table3 = PrettyTable(['随机特征个数', '误差率'])
    for label, clf in ensemble_clfs:
        # for i in range(min_estimators, max_estimators + 1):
        #     clf.set_params(n_estimators=i)
        clf.fit(X, y)

        # Record the OOB error for each `n_estimators=i` setting.
        oob_error = 1 - clf.oob_score_
        error_rate[label].append((round(oob_error, 4)))
        # print(label)
        # print(round(oob_error,4))
        table3.add_row([label, round(oob_error, 4)])
    print(table3)
    print()


# 打印混淆矩阵
def print_mxjuzhen(result, forest):
    print('------------ 随机森林模型混淆矩阵 ------------')
    table = con(y_test, result)
    table_x = PrettyTable(['实际类别', '预测适宜', '预测不适宜', '分类误差率(%)'])
    table_x.add_row(["适宜", table[0][0], table[0][1], round(table[0][1] / table[0][0]*100, 2)])
    table_x.add_row(["不适宜", table[1][0], table[1][1], round(table[1][0] / table[1][1]*100, 2)])
    print(table_x)
    score = forest.score(X_test, y_test)    # 测试准确率
    print('准确率： ' + str(round(score, 2)) + '\n')


# 画出决策树
def draw_tree():
    feat_labels = traindata_all.columns[1:len(traindata_all.columns) - 1]
    X_lables = [x for x in feat_labels]
    y_lables = traindata_all.columns[len(traindata_all.columns) - 1]

    # 接着，构建决策树模型
    model_tree = DecisionTreeClassifier()
    model_tree.fit(X_train, y_train)

    # # 评价模型准确性
    # y_prob = model_tree.predict_proba(X_test)[:, 1]
    # y_pred = np.where(y_prob > 0.5, 1, 0)
    # model_tree_score = model_tree.score(X_test, y_pred)
    # print('模型准确性：' + str(model_tree_score))

    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    dot_tree = tree.export_graphviz(model_tree, out_file=None, feature_names=X_lables, class_names=y_lables,
                                    filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_tree)
    img = Image(graph.create_png())
    # 设置决策树名称和输出路径
    graph.write_png("D:/out12121.png")



if __name__ == '__main__':
    # 获取数据
    traindata_all = pd.read_csv("D:/data24.csv")
    traindata_all.columns = ["ID", "TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP", "SLP", "SI"]

    # 将数据集分为训练集和测试集
    X, y = traindata_all.iloc[:, 1:len(traindata_all.columns) - 1].values, traindata_all.iloc[:, len(traindata_all.columns) - 1].values     # 选择评价特征和标签特征
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 打印评价特征和标签特征
    print_featurelable()

    # 建立模型
    forest, result = build_model()

    # 交叉验证
    cross_validation()

    # 打印混淆矩阵
    print_mxjuzhen(result, forest)

    # 分类树数量和误差率的关系
    findbest_n_estimators(100)

    # 不同max_features取值对应误差大小
    findbest_maxfeatures()

    # 因子重要性判断
    top_variable_importance(forest)

    # 画出决策树
    draw_tree()
