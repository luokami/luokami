"""
肘方法选择最优K值超参数:
    1. 遍历 自定义的K值列表
    2. 训练Kmeans模型, 获取sse值, 添加到列表中
    3. 绘制肘方法图
    4. 选择肘部位置的K值
构造一个数据集, 使用kmeans进行聚类分析
    1. 构造数据
    2. 绘制数据分布
    3. 使用kmeans进行聚类分析
    4. 绘制聚类结果
    5. 评估聚类结果
"""
import os
os.environ["OMP_NUM_THREADS"] = "4"
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 1.构造数据
# n_samples: 样本数量, n_features: 特征数量, centers: 聚类中心数量, cluster_std: 聚类中心方差
x, y = make_blobs(n_samples=1000, n_features=2, centers=[(-1, -1), (0, 0), (1, 1), (2, 2)],cluster_std=[0.4, 0.2, 0.2, 0.2], random_state=9)

# 2. 遍历 自定义的K值列表, 使用kmeans进行聚类分析
# 初始化存储sse值的列表
sse_res = []
# 循环遍历(1, 100)k值, 进行kmeans训练, 获取sse值, 添加到列表中
for k in range(1, 100):
    kmeans = KMeans(n_clusters=k, max_iter=100, random_state=9)
    kmeans.fit(x)
    # 获取sse值: kmeans.inertia_属性就是sse值
    sse_res.append(kmeans.inertia_)

# 3. 绘制肘方法图
plt.figure(figsize=(18, 8), dpi=100)
# 'or-': 红色点虚线
plt.plot(range(1, 100), sse_res, 'or-')
plt.title("sse")
plt.xticks(range(0, 100, 4), labels=range(0, 100, 4))
plt.grid()
plt.xlabel("K clusters")
plt.ylabel("SSE")
plt.show()

