"""
KNN算法的api使用: KNeighborsClassifier, KNeighborsRegressor
"""

# 分类任务
from sklearn.neighbors import KNeighborsClassifier

# 1. 准备数据
x = [[1], [2], [3], [4]]
y = [0, 0, 1, 1]

# 2. 模型训练
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(x, y)

# 3. 模型预测
print(knn.predict([[5]]))  # 需要传入二维数据的特征


# 回归任务
from sklearn.neighbors import KNeighborsRegressor

# 1. 准备数据
X = [[0, 0, 1],
     [1, 1, 0],
     [3, 10, 10],
     [4, 11, 12]]
y = [0.1, 0.2, 0.3, 0.4]

# 2. 模型训练
knn = KNeighborsRegressor(n_neighbors=2)
knn.fit(X, y)

# 3. 模型预测
print(knn.predict([[1, 1, 3]]))  # 回归, 最近邻的值进行平均
print(knn.predict([[4, 10, 11]]))  # 回归, 最近邻的值进行平均