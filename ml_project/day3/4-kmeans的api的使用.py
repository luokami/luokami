"""
构造一个数据集，使用kmeans进行聚类分析
    1.构造数据
    2.绘制数据分布
    3.使用kmeans进行聚类分析
    4.绘制聚类结果
    5.评估聚类结果
"""
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.metrics import calinski_harabasz_score


# 1.构造数据
#n_samples:样本数量,n_features:特征数量,centers:聚类中心数量,cluster_std:聚类中心方差
x, y = make_blobs(n_samples=1000, n_features=2, centers=[(-1, -1), (0, 0), (1, 1), (2, 2)],cluster_std=[0.4, 0.2, 0.2, 0.2], random_state=9)

# print(x) #x 1000条样本，每个样本2个特征
# print(y) #y 聚类中心索引

# 2.绘制数据分布
plt.figure()
plt.scatter(x[:, 0], x[:, 1], marker='o')
plt.show()

# 3.使用kmeans进行聚类分析
y_pred = KMeans(n_clusters=3,random_state=9).fit_predict(x)
# 4.绘制聚类结果
plt.scatter(x[:, 0], x[:, 1], c=y_pred)
plt.show()

# 5.评估聚类结果
score = calinski_harabasz_score(x,y_pred)
print(score)