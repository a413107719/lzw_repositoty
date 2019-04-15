import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import graphviz
import pydotplus
from sklearn import tree
from IPython.display import Image
import os


# 获取数据
traindata_all = pd.read_csv("D:/data24.csv")
traindata_all.columns = ["ID", "TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP",
                         "SLP", "SI"]
# 将数据集分为训练集和测试集
X, y = traindata_all.iloc[:, 1:len(traindata_all.columns) - 1].values, traindata_all.iloc[:, len(
    traindata_all.columns) - 1].values  # 选择评价特征和标签特征
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
# columns = X


feat_labels = traindata_all.columns[1:len(traindata_all.columns) - 1]
X_lables = str([x for x in feat_labels])
y_lables = str(traindata_all.columns[len(traindata_all.columns) - 1])

# 接着，构建决策树模型
model_tree = DecisionTreeClassifier()
model_tree.fit(X_train, y_train)


# # 评价模型准确性
# y_prob = model_tree.predict_proba(X_test)[:,1]
# y_pred = np.where(y_prob > 0.5, 1, 0)
# model_tree_score = model_tree.score(X_test, y_pred)
# print('模型准确性：' + str(model_tree_score))


os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
dot_tree = tree.export_graphviz(model_tree,out_file=None,feature_names=X_lables,class_names=y_lables,filled=True, rounded=True,special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_tree)
img = Image(graph.create_png())
graph.write_png("out.png")