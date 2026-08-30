"""
客户分群分析案例:
    1. 加载数据
    2. 肘方法和轮廓系数选择K值超参数
    3. Kmeans聚类分析
    4. 绘制聚类结果
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


# 1. 加载数据
data = pd.read_csv('customers.csv')
print(data.head())
data.info()

# 2. 肘方法和轮廓系数选择K值超参数
# 获取训练数据
X = data.iloc[:, [3, 4]]
# 初始化肘方法和轮廓系数结果列表
sse = []
sc = []

# 遍历[2, 11)k值, 计算sse, sc, 因为sc最小聚类数量需要大于1
for k in range(2, 11):
    km = KMeans(n_clusters=k, max_iter=100, random_state=22)
    km.fit(X)
    # sse和sc结果添加到列表中
    sse.append(km.inertia_)
    pred = km.predict(X)
    sc.append(silhouette_score(X, pred))

# 绘制肘方法和轮廓系数图
# 定义画布
fig = plt.figure(figsize=(20, 10))
# 添加子图1: 肘方法图
ax1 = fig.add_subplot(1, 2, 1)  # 第一个值是序号, 第二个值是行数, 第三个值是列数
ax1.plot(range(2, 11), sse)
ax1.set_xlabel('Number of clusters')
ax1.set_ylabel('SSE')
ax1.grid()

# 添加子图2: 轮廓系数图
ax2 = fig.add_subplot(2, 2, 1)
ax2.plot(range(2, 11), sc)
ax2.set_xlabel('Number of clusters')
ax2.set_ylabel('Silhouette Coefficient')
ax2.grid()

plt.show()

















