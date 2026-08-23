"""
波士顿案例: cart树, 回归任务
    步骤:
        1. 导包
        2. 数据集划分
        3. 标准化
        4. 模型训练
        5. 模型评估
"""

# 1. 导包
# from sklearn.datasets import load_boston                # 数据(), 数据集废弃
from sklearn.preprocessing import StandardScaler        # 特征处理
from sklearn.model_selection import train_test_split    # 数据集划分
from sklearn.linear_model import LinearRegression       # 正规方程的回归模型
from sklearn.linear_model import SGDRegressor           # 梯度下降的回归模型
from sklearn.metrics import mean_squared_error, mean_absolute_error, root_mean_squared_error  # 均方误差评估

# 官方推荐加载波士顿案例数据方式:
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)
print(raw_df)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# 2. 数据集划分
# train_test_split参数依次, 特征, 标签, random_state: 随机种子: 为了每次随机得到同样的划分结果, 为了复现模型训练
x_train, x_test, y_train, y_test = train_test_split(data, target, random_state=22)

# 3. 标准化
# 实例化标准化对象
scalar = StandardScaler()
# fit_transform:  训练集特征的标准化训练和转换同时做
x_train = scalar.fit_transform(x_train)
# 已经训练好的scalar, 直接对测试集特征进行转换就可以了
x_test = scalar.transform(x_test)

# 4. 模型训练
# 实例化模型
dtr = DecisionTreeRegressor(criterion='squared_error', max_depth=5)
# 训练
dtr.fit(x_train, y_train)

# 5. 模型评估
# 预测
y_pred = dtr.predict(x_test)
# 评估
loss = mean_squared_error(y_test, y_pred)
print("评估损失: ", loss)  # 评估损失:  34.32740174726683

# 6. 绘制图像
plt.figure(figsize=(100, 80), dpi=150)
plot_tree(
    dtr,
    max_depth=10,  # 树深度
    filled=True,  # 填充颜色, 颜色深浅代表节点纯度
)
plt.savefig("data/Boston.png", dpi=150)
plt.show()