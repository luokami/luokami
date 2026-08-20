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
from sklearn.metrics import mean_squared_error  # 计算均方误差
# from sklearn.model_selection import train_test_split


# 1. 创建数据集
np.random.seed(666)  # 指定随机种子
x = np.random.uniform(-3, 3, size=100)  # -3, 3区间 100个 均匀分布的随机值
# np.random.normal: 正态分布
y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, size=100)
# 2. 模型训练
lr = LinearRegression()
X = x.reshape(-1, 1)  # 转成二维数组
lr.fit(X, y)
# 3. 模型预测
pred = lr.predict(X)
# print(pred)
# 预测误差
error = mean_squared_error(y, pred)
print("预测误差: ", error)
# 4. 绘制图像
plt.scatter(x, y)  # 原始数据散点图
plt.plot(x, pred, c='r')  # 预测折线图
plt.show()
