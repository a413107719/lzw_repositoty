# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 导入数据集
data = pd.read_csv("D:/data23.csv")
# 划分训练集和测试集数据
train_data, test_data = train_test_split(data, test_size=0.2)   # 参数：test_size
