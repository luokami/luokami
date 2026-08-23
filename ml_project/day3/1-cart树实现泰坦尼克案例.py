"""
实现泰坦尼克案例:
    1. 数据加载
    2. 数据预处理
    3. 特征工程
    4. 模型训练
    5. 模型评估
    6. 模型预测
    7. 绘制图像
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# 1. 数据加载
titanic = pd.read_csv('data/train.csv' )
# print(titanic.head())
# titanic.info()

# 2. 数据预处理
x = titanic[['Pclass', 'Sex', 'Age']].copy()
y = titanic['Survived']
x['Age'] = x['Age'].fillna(value=x['Age'].mean()) # fillna: 对缺失值填充均值
x.info()

# 3. 特征工程
# 把Sex列的字符串值转换为0/1, 使用get_dummies进行one-hot编码
x = pd.get_dummies(x)  # 特征有几个类别, 就会转成几列, 样本本身属于哪个类别, 这个类别赋值为1, 其他类别都为0
print(x.head())
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=22)

# 4. 模型训练
# criterion: 指定分割节点的指标, 默认是'gini', 还可以是'entropy', max_depth: 指定树的最大深度
dtc = DecisionTreeClassifier(criterion='gini')
dtc.fit(x_train, y_train)

# 5. 模型评估
# 准确率
accuracy = dtc.score(x_test, y_test)
print("Accuracy:", accuracy)
# 指标报告
y_pred = dtc.predict(x_test)
report = classification_report(y_test, y_pred)
print(report)

# 6. 绘制图像
plt.figure(figsize=(100,100), dpi=150)
plot_tree(
    dtc,
    max_depth=10,  # 树深度
    filled=True,  # 填充颜色, 颜色深浅代表节点纯度
    feature_names=x.columns,  # 特征名称
    class_names=["died", "survived"]  # 类别名称
)
# plt.savefig('data/titanic_dtc.png', dpi=150)
plt.show()