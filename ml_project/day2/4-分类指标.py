"""
分类指标: 混淆矩阵: 行表示真实值, 列表示预测值, 组合成4个指标: TP, TN, FP, FN  (T: True, F: False, P: Positive, N: Negative)
"""

from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
import pandas as pd

#绘制混淆矩阵
# 真实标签
y_true = ["恶性", "恶性", "恶性", "恶性", "恶性", "恶性", "良性", "良性", "良性", "良性"]
# 指定标签类别以及显示名称
labels = ["恶性", "良性"]
df_labels = ["恶性(正例)", "良性(反例)"]

# 模型A的预测结果
y_pred_A = ["恶性", "恶性", "恶性", "良性", "良性", "良性", "良性", "良性", "良性", "良性"]
cm = confusion_matrix(y_true, y_pred_A, labels=labels)
cm_df = pd.DataFrame(cm, index=df_labels, columns=df_labels)
print("A模型的混淆矩阵:\n", cm_df)
#计算A模型的准确率
acc_A = accuracy_score(y_true, y_pred_A)
#计算A模型的精确率
prec_A = precision_score(y_true, y_pred_A, pos_label="恶性")
#计算A模型的召回率
rec_A = recall_score(y_true, y_pred_A, pos_label="恶性")
#计算A模型的F1分数
f1_A = f1_score(y_true, y_pred_A, pos_label="恶性")
print("A模型的准确率:", acc_A,"A模型的精确率:", prec_A,"A模型的召回率:", rec_A,"A模型的F1分数:", f1_A)



# 模型B的预测结果
y_pred_B = ["恶性", "恶性", "恶性", "恶性", "恶性", "恶性","恶性", "恶性", "恶性", "良性"]
cm = confusion_matrix(y_true, y_pred_B, labels=labels)
cm_df = pd.DataFrame(cm, index=df_labels, columns=df_labels)
print("B模型的混淆矩阵:\n", cm_df)
#计算B模型的准确率
acc_B = accuracy_score(y_true, y_pred_B)
#计算B模型的精确率
prec_B = precision_score(y_true, y_pred_B, pos_label="恶性")
#计算B模型的召回率
rec_B = recall_score(y_true, y_pred_B, pos_label="恶性")
#计算B模型的F1分数
f1_B = f1_score(y_true, y_pred_B, pos_label="恶性")
print("B模型的准确率:", acc_B,"B模型的精确率:", prec_B,"B模型的召回率:", rec_B,"B模型的F1分数:", f1_B)

