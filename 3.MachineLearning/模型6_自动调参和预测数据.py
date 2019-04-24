from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.model_selection import train_test_split

# 获取数据
data_train = pd.read_csv("F:/data.csv")
data_predict = pd.read_csv("F:/test.csv")
print(data_train.head())
print('......')
print()
print(data_train.describe())
print()

# 特征因子
feature_column = [x for x in data_train.columns[1:len(data_train.columns) - 1]]
# ID
ID = data_train.columns[0]
# 标签因子
lable_column = data_train.columns[len(data_train.columns) - 1]
print(feature_column, lable_column, sep='\n')
print()

# 删除ID字段和标签字段，只留训练数据
X = data_train.drop([lable_column, ID], axis=1)
y = data_train[lable_column]
p = 0.3  # 验证数据占比（参数）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=p, random_state=23)


# 选择分类器的类型
forest = RandomForestClassifier()
# 可以通过定义树的各种参数，限制树的大小，防止出现过拟合现象
# 模型需要运行两次，第一次树的数量默认值为10，第二次根据可视化图输入最合适值。
parameters = {'n_estimators': [10, 100],
              'max_features': ['log2', 'sqrt','auto'],
              'criterion': ['entropy', 'gini'],        #分类标准用熵，基尼系数
              'max_depth': [2, 3, 5, 10],
              'min_samples_split': [2, 3, 5],
              'min_samples_leaf': [1, 5, 8]
             }
# 以下是用于比较参数好坏的评分，使用'make_scorer'将'accuracy_score'转换为评分函数
acc_scorer = make_scorer(accuracy_score)
# 自动调参，GridSearchCV，它存在的意义就是自动调参，只要把参数输进去，就能给出最优化的结果和参数
# GridSearchCV用于系统地遍历多种参数组合，通过交叉验证确定最佳效果参数。
grid_obj = GridSearchCV(forest, parameters, scoring=acc_scorer)
grid_obj = grid_obj.fit(X_train, y_train)
# 将forest设置为参数的最佳组合
forest = grid_obj.best_estimator_
print("建树参数:", forest, sep='\n')
# 将最佳算法运用于随机森林，随机森林建树
forest.fit(X_train, y_train)

# 测试数据
predictions = forest.predict(X_test)
print(accuracy_score(y_test, predictions))

# 模型预测
predictions = forest.predict(data_predict.drop(ID, axis=1))  # 删除ID字段
output = pd.DataFrame({'id': data_predict[ID], 'prediction': predictions})
output.to_csv(r'F:\ceshi2.csv')
output.head()
