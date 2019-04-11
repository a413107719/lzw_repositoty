# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation, metrics


# 导入数据集
data = pd.read_csv("D:/data23.csv")
predictors = ["TR", "TCH", "FZZ", "MZ", "SLH", "TRJ", "TRS", "SJD", "JMD", "DM", "PW", "ELE", "ASP", "SLP"]
x = data[predictors]
y = data['SI']

# 划分训练集和测试集数据
train_data, test_data = train_test_split(data, test_size=0.2)   # 参数

# 随机森林框架参数选取
# n_estimators:森林中决策树的个数（有的地方称为ntree），默认是10。一般来说n_estimators太小，容易欠拟合，n_estimators太大，计算量会太大
# oob_score:是否采用袋外样本来评估模型的好坏。默认值False,推荐设置为True,因为袋外分数反应了一个模型拟合后的泛化能力。
# criterion:CART树划分时对特征的评价标准。分类RF默认是基尼系数gini,回归RF默认是均方差mse。
# bootstrap: boolean类型取值，表示是否采用有放回式的抽样方式，默认True

# 随机森林决策树参数选取
# max_features：寻求最佳分割时的考虑的特征数量（有的地方称为mtry），即特征数达到多大时进行分割。
    # int: 特征绝对数，float: 总特征数的百分比， "auto": 等于sqrt(N)， "sqrt": 同等于"auto"， "log2": 对于log2(N)，None: 等于N
# max_depth：决策树最大深度，int或者None。一般数据少或者特征少的时候可以不管这个值。
# min_samples_split：分割内部节点所需的最少样本数量，int或float，默认为2，若样本不大，可忽略
# min_samples_leaf：叶子节点最少样本数，int或float，默认为1，若样本不大，可忽略
# min_weight_fraction_leaf:能成为叶子节点的条件是该节点对应的实例数和总样本数的比值，至少大于这个值，默认是0
# max_leaf_nodes：最大叶子节点数，通过限制最大叶子节点数防止过拟合。如果加了限制，算法会建立在最大叶子节点数内最优的决策树。默认是"None”，若特征不多，可忽略
# min_impurity_split：节点划分最小不纯度，这个值限制了决策树的增长，如果某节点的不纯度（基于基尼系数，均方差）小于这个阈值，则该节点不再生成子节点，一般不推荐改动默认值


target='SI'
IDcol = 'ID'
print('表征特征统计：')
print(data['SI'].value_counts())
print()

# 对比不同分类树数量，误差率大小，以确定最优n_estimators数量
for i in range(9):
    tree_number = 20+10*i
    rf0 = RandomForestClassifier(oob_score=True, random_state=10, max_features=10, n_estimators=tree_number)
    rf0.fit(x, y)
    print(tree_number)
    print(rf0.oob_score_)
# todo:绘制“分类树数量对应误差率折线图”

# param_test1 = {'n_estimators': list(range(10, 71, 10))}
# gsearch1 = GridSearchCV(estimator = RandomForestClassifier(min_samples_split=100,
#                                   min_samples_leaf=20,max_depth=8,max_features='sqrt' ,random_state=10),
#                        param_grid = param_test1, scoring='roc_auc',cv=5)
# gsearch1.fit(x,y)
# print(gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_)


param_test2 = {'max_depth':list(range(3,14,2)), 'min_samples_split':list(range(50,201,20))}
gsearch2 = GridSearchCV(estimator = RandomForestClassifier(n_estimators= 60,
                                  min_samples_leaf=20,max_features='sqrt' ,oob_score=True, random_state=10),
   param_grid = param_test2, scoring='roc_auc',iid=False, cv=5)
gsearch2.fit(x,y)
print(gsearch2.grid_scores_, gsearch2.best_params_, gsearch2.best_score_)




# todo:对比不同随机特征(max_features)取值,误差率大小，以确定最优随机特征个数
# todo:交叉验证:得到信息增益最大的那棵树
# todo:数据验证：用混淆矩阵判断模型的泛化程度
# todo:因子重要性判断：得到因子重要性排序表
# todo:单因子影响程度


# 绘图：
# 可视化随机森林中的一棵树： https://www.jianshu.com/p/58815b3e761c
