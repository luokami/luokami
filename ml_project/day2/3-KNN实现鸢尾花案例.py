"""
KNN算法实现鸢尾花分类:
    1. 导入数据集
    2. 数据预处理
    3. 特征工程->特征预处理->标准化
    4. 训练模型
    6. 预测
    7. 评估模型
"""

from sklearn.datasets import load_iris
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

def data_show():
    # 1. 导入数据集, 查看
    iris = load_iris()
    # 查看数据集形状
    print(iris.data.shape)
    print('=' * 60)
    # 查看特征
    print(iris.data[:5])
    print('=' * 60)
    # 查看标签
    print(iris.target)
    print('=' * 60)
    # 查看特征名称
    print(iris.feature_names)
    print('=' * 60)
    # 查看标签名称
    print(iris.target_names)
    print('=' * 60)
    # 查看数据集描述
    print(iris.DESCR)
    print('=' * 60)
    # 查看数据集名称
    print(iris.filename)

def image_show():
    # 1.导出数据集
    iris = load_iris()
    feature_name = iris.feature_names

    # 2.转为dataframe格式
    df = pd.DataFrame(iris.data, columns=feature_name)
    # 特征的df添加标签
    df['target'] = iris.target

    # 3.可视化
    x_label = 'sepal length (cm)'
    y_label = 'petal width (cm)'

    # 使用seaborn绘制散点图,hue表示不同标签用不同颜色表示,fit_tag表示是否绘制回归线
    sns.lmplot(x=x_label, y=y_label, data=df, hue='target', fit_reg=False)
    plt.xlabel = x_label
    plt.ylabel = y_label
    # plt.legend()
    plt.title("Iris Data Visualization")
    plt.show()

def knn_iris():
    # 1.导入数据集
    iris = load_iris()
    # 2.数据预处理->数据集划分
    # test_size = 0.3数据集划分比例:7:3, random_state = 22 每个种子对应一个随机结果
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=22)
    print("X_train shape:", x_train.shape)
    print('X_test shape:', x_test.shape)
    # 3.特征工程->特征预处理(标准化)
    scaler = StandardScaler()
    # 训练集标准化
    x_train = scaler.fit_transform(x_train)
    # 测试集标准化.直接套用训练集fit的结果,转换测试集
    x_test = scaler.transform(x_test)
    # 4.训练模型
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)
    # 5.模型评估
    # ① .使用model.score-->获取准确率
    acc = knn.score(x_test, y_test)  # 两个参数依次: 测试集特征, 测试集标签
    print("Score Accuracy:", acc)
    # ② .使用accuracy_score-->获取准确率
    y_pred = knn.predict(x_test)
    acc = accuracy_score(y_test, y_pred)  # 两个参数依次: 真实值, 预测值
    print("Accuracy Score:", acc)
    # 6.模型预测
    mydata = [[5.1, 3.5, 1.4, 0.2],
              [4.6, 3.1, 1.5, 0.2]]
    # 预测特征标准化(预测数据要保持和训练数据格式一样)
    mydata = scaler.transform(mydata)
    # 模型预测
    # 预测标签
    y_pred = knn.predict(mydata)
    print("Predicted labels:", y_pred)
    # 预测概率
    y_prob = knn.predict_proba(mydata)
    print("Predicted probabilities:", y_prob)

def gridsearchCV_iris():
    # 1. 导入数据集
    iris = load_iris()
    print("Iris data shape:", iris.data.shape)
    # 2. 数据预处理->数据集划分
    # test_size=0.3 数据集划分比例: 7: 3, random_state=22, 每个种子对应一个随机结果
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=22)
    print("X_train shape:", x_train.shape)
    print('X_test shape:', x_test.shape)
    # 3. 特征工程-->特征预处理(标准化)
    scalar = StandardScaler()
    # 训练集标准化
    x_train = scalar.fit_transform(x_train)
    # 测试集标准化, 直接套用训练集fit的结果, 转换测试集
    x_test = scalar.transform(x_test)
    # 4. 训练模型
    # knn = KNeighborsClassifier()
    # # knn.fit(x_train, y_train)
    # # 4.1 网格搜索CV
    # param_dict = {"n_neighbors": [1, 5, 7, 8]} # 多个超参数的候选值字典
    # knn = GridSearchCV(knn, param_grid=param_dict, cv=5) #cv:5折交叉验证
    # knn.fit(x_train, y_train)
    # print("Best params:", knn.best_params_)
    # print("Best score:", knn.best_score_) #best score:0.9523809523809523
    # print("Best estimator:", knn.best_estimator_)
    # print("Best cv results:", knn.cv_results_)

    # 选择最优的超参数组合,重新训练模型
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)

    # 5. 模型评估
    # ① 使用model.score --> 获取准确率
    acc = knn.score(x_test, y_test)  # 两个参数依次: 测试集特征, 测试集标签
    print("knn.Score Accuracy:", acc)
    # ② 使用accuracy_score 获取准确率
    y_pred = knn.predict(x_test)
    acc = accuracy_score(y_test, y_pred)  # 两个参数依次: 真实值, 预测值
    print("Accuracy Score:", acc)
    # 6. 模型预测
    mydata = [[5.1, 3.5, 1.4, 0.2],
              [4.6, 3.1, 1.5, 0.2]]
    # 预测特征标准化(预测数据要保持和训练数据格式一样)
    mydata = scalar.transform(mydata)
    # 模型预测
    # 预测标签
    y_pred = knn.predict(mydata)
    print("Predicted labels:", y_pred)
    # 预测概率
    y_prob = knn.predict_proba(mydata)
    print("Predicted probabilities:", y_prob)

if __name__ == '__main__':
    # data_show()
    # image_show()
    # knn_iris()
    gridsearchCV_iris()
