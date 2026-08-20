"""
线性回归API使用示例: 预测波仔体重案例
    步骤:
    1. 导入所需的库
    2. 准备数据集
    3. 实例化模型
    4. 模型训练
    5. 模型预测
"""

# 1. 导入所需的库
from sklearn.linear_model import LinearRegression

# 2. 准备数据集
x = [[160], [166], [172], [174], [180]]
y = [56.3, 60.6, 65.1, 68.5, 75]
# 3. 实例化模型
model = LinearRegression()
# 4. 模型训练
# 所有机器学习模型都有fit方法，用来训练模型，传入特征和标签
model.fit(x, y)
# 打印训练的权重和偏置
print(model.coef_)  # 斜率/权重
print(model.intercept_)  # 截距/偏置
# 5. 模型预测
# 模型都有predict方法，传入特征需要是二维数组
result = model.predict([[176]])
print(result)
