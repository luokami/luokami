"""
归一化: 将数据缩放到一个特定的范围，通常是0到1之间。
公式: x' = (x - min) / (max - min) --> [0, 1],  x'' = x' * (mx - mi) + mi  --> [mi, mx]
标准化: 将数据转换为均值为0，标准差为1的标准分布。
公式: x' = (x - mean) / std
"""

# 归一化
from sklearn.preprocessing import MinMaxScaler

# 准备数据
data = [[90, 2, 10, 40],
        [60, 4, 15, 45],
        [75, 3, 13, 46]]

# 实例化归一化对象
scalar = MinMaxScaler(feature_range=(0, 1))
data = scalar.fit_transform(data)

print(data)


# 标准化
from sklearn.preprocessing import StandardScaler

# 准备数据
data = [[90, 2, 10, 40],
        [60, 4, 15, 45],
        [75, 3, 13, 46]]

# 实例化归一化对象
scalar = StandardScaler()
data = scalar.fit_transform(data)

print(data)