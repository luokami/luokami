"""
绘制欠拟合图像:
    1. 创建数据集
    2. 模型训练
    3. 模型预测
    4. 绘制图像
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error # 计算均方误差
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge

# 1. 创建数据集
np.random.seed(666)  # 指定随机种子
x = np.random.uniform(-3, 3, size=100)  # -3, 3 区间 100个 均匀分布的随机值
# np.random.normal: 正态分布
y = 0.5 * x ** 2 + x + 2 + np.random.normal(0,1, size=100)
# 2. 模型训练
lr = Ridge(alpha=1)
X = x.reshape(-1, 1)  # 转成二维数组
# 增加二次项x的特征, hstack: 水平拼接
X = np.hstack([X, X ** 2, X ** 3, X ** 4, X ** 5, X ** 6, X ** 7, X ** 8, X ** 9, X ** 10])
lr.fit(X, y)
# 打印模型权重
print(lr.coef_)
"""
[ 9.98585594e-01  9.69552419e-01  6.91716587e-02 -3.74558751e-01
 -3.79854415e-02  1.16753582e-01  7.62797792e-03 -1.51421382e-02
 -5.02418496e-04  6.85026000e-04]
"""
# 3. 模型预测
pred = lr.predict(X)
# print(pred)
# 预测误差
error = mean_squared_error(y, pred)
print("预测误差: ", error)  # 预测误差:  1.0677393926180387
# 4. 绘制图像
plt.scatter(x, y)  # 原始数据散点图
# plt.plot(x, pred, c='r')  # 预测折线图
# 按照x的顺序排序, np.sort对x排序, np.argsort获取x的排序后索引
plt.plot(np.sort(x), pred[np.argsort(x)], c='r')
plt.show()