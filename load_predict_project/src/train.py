"""
模型训练模块:
    1. 定义模型训练类, 初始化日志, 加载数据
    2. 探索性数据分析
    3. 特征工程
    4. 模型训练
"""
# 文件操作
import os
# 数据处理
import pandas as pd
# 可视化
import matplotlib.pyplot as plt
# 时间处理
import datetime
# 自定义日志模块
from utils.log import Logger
# 自定义数据处理模块
from utils.common import data_preprocessing
# 集成学习模型
# 安装xgboost库, pip install xgboost
from xgboost import XGBRegressor
# 分割数据集
from sklearn.model_selection import train_test_split
# 网格搜索, 超参数优化
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
# 模型评估指标
from sklearn.metrics import mean_squared_error, mean_absolute_error
# 模型保存, 加载
import joblib

# 设置中文显示，避免中文显示为方块
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15
pd.set_option('display.max_columns', None)


# 1.定义模型训练类, 初始化日志, 加载数据
class PowerLoadModel:
    def __init__(self, data_path):
        # 初始化日志
        log_file = "train_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.logger = Logger("../", log_file).get_logger()

        # 加载数据
        self.source_data = data_preprocessing(data_path)
        # 初始化time对应load的字典
        self.time_key_load = self.source_data.set_index('time')['power_load'].to_dict()
        # print("时间对应load的字典: ", self.time_key_load)

    # 2.探索性数据分析
    def ana_data(self):
        self.logger.info("=======================开始进行探索性数据分析========================")
        # 1.负荷整体的分布情况
        fig = plt.figure(figsize=(20, 30))
        ax1 = fig.add_subplot(411)  # 4个子图, 第一行 第一个
        # 绘制负荷直方图, 展示负荷整体分布情况
        ax1.hist(self.source_data['power_load'])
        ax1.set_title("负荷整体分布情况")
        ax1.set_xlabel("负荷")
        ax1.set_ylabel("频率")

        # 2.各个小时的平均负荷趋势，看一下负荷在一天中的变化情况
        data = self.source_data.copy()  # 对源数据改变的时候, 最好先进行copy(默认深拷贝)，避免数据混乱
        # 获取小时信息，pandas中series获取小时信息，series.dt.属性;pandas获取单个str类型时间数据,pd.to_datatime(time_str).属性
        data['hour'] = data.time.dt.hour
        # 按小时分组, 计算每个小时的平均负荷, as_index=False表示不将小时作为索引
        per_time_df = data.groupby(data.hour, as_index=False)['power_load'].mean()
        # print(per_time_df)

        ax2 = fig.add_subplot(412)  # 4行1列,第二个子图
        ax2.plot(per_time_df.hour, per_time_df.power_load)
        ax2.set_title("各个小时的平均负荷趋势")
        ax2.set_xlabel("小时")
        ax2.set_ylabel("平均负荷")
        ax2.set_xticks(range(24))
        plt.grid()

        # 3.各个月份的平均负荷趋势，看一下负荷在一年中的变化情况
        # 提取月份信息,pandas中series获取月份信息，series.dt.属性;pandas获取单个str类型时间数据,pd.to_datatime(time_str).属性
        data['month'] = data.time.dt.month
        # 按月份分组, 计算每个月份的平均负荷, as_index=False表示不将月份作为索引
        per_month_df = data.groupby(data.month, as_index=False)["power_load"].mean()
        # print(per_month_df)

        ax3 = fig.add_subplot(413)  # 4行1列, 第三个子图
        ax3.plot(per_month_df.month, per_month_df.power_load)
        ax3.set_title("各个月份的平均负荷趋势")
        ax3.set_xlabel("月份")
        ax3.set_ylabel("平均负荷")
        ax3.set_xticks(range(1, 13))
        plt.grid()

        # 4.工作日与周末的平均负荷情况，看一下工作日的负荷与周末的负荷是否有区别
        # 获取当前时间是周几
        data['weekday'] = data.time.dt.weekday  # 0-6, 5, 6是周末
        # print(data.head())
        data['weekend'] = data.weekday.apply(lambda x: 1 if x in [5, 6] else 0)
        workday_load = data[data['weekend'] == 0]['power_load'].mean()
        weekend_load = data[data['weekend'] == 1]['power_load'].mean()
        # print(data)

        ax4 = fig.add_subplot(414)  # 4行1列, 第四个子图
        ax4.bar(['工作日', '周末'], [workday_load, weekend_load])
        ax4.set_title("工作日与周末的平均负荷情况")
        ax4.set_ylabel("平均负荷")
        plt.show()

        self.logger.info("===========================探索性数据分析完成=============================")
        """
        负荷对于24小时和12个月存在周期性变化关系, 可以作为比较强的回归预测特征, 工作日和周末对负荷影响差不多, 不是一个好的预测特征 
        """

    # 3.特征工程
    def feature_engineering(self):
        self.logger.info("=======================开始进行特征工程========================")
        # 对给定的数据源，进行特征工程处理，提取出关键的特征
        # 1.提取出时间特征：小时、月份
        data = self.source_data.copy()
        data['hour'] = data.time.dt.hour
        data['month'] = data.time.dt.month

        # 2.提取出相近时间窗口中的负荷特征：step大小窗口的负荷
        # 获取前1小时的时间
        for k, v in [("前1小时", 1), ("前2小时", 2), ("前3小时", 3)]:
            last_n_hour = data.time - pd.Timedelta(v, unit='h')  # series
            # 获取不到返回None, 最前面1天和前3个小时的数据会产生None
            last_n_load = last_n_hour.apply(lambda x: self.time_key_load.get(x))
            data[k] = last_n_load

        # print(data.head())

        # 3.提取昨日同时刻负荷特征
        # 获取前1天的同时刻时间
        # last_1_day = data.time - pd.Timedelta(1, unit='d')
        last_1_day = data.time - pd.Timedelta(days=1)
        # 获取不到返回None, 最前面1天和前3个小时的数据会产生None
        # 使用time-load字典获取前一天对应时刻的负荷
        # last_1_load = last_1_day.apply(lambda x: self.time_key_load.get(x))
        last_1_load = last_1_day.map(self.time_key_load)  # map处理单列数据,效率高
        data['yesterday_load'] = last_1_load

        # 4.剔除出现空值的样本
        data.dropna(inplace=True)  # 原地删除空值

        # 5.整理时间特征，并返回
        data = pd.get_dummies(data, columns=['hour', 'month'])  # onehot编码
        # print(data.head())
        print(data.columns.tolist())

        self.logger.info("=======================特征工程完成=============================")
        # 返回特征，标签，列名
        return data.iloc[:, 2:], data.iloc[:, 1], data.columns[2:]

    # 4.模型训练
    def model_train(self):
        # 1.数据集切分
        x, y, feature_name = self.feature_engineering()
        # 时间序列预测，划分数据集必须按照时间顺序划分，测试集必须在训练集之后
        train_size, val_size, test_size = (int(len(x) * 0.6), int(len(x) * 0.2),
        len(x) - int(len(x) * 0.6) - int(len(x) * 0.2))  # 训练集、验证集、测试集比例
        x_train, x_val, x_test = (x.iloc[:train_size, :], x.iloc[train_size:train_size+val_size, :],x.iloc[train_size+val_size:, :])
        y_train, y_val, y_test = (y.iloc[:train_size], y.iloc[train_size:train_size+val_size],y.iloc[train_size+val_size:])

        # 2.网格化搜索与交叉验证
        # 定义xgb模型，指定超参数，迭代数量的上限1000，早停(防止过拟合)轮数20:连续20轮训练指标没有提升则停止训练
        # xgb = XGBRegressor(n_estimators=1000,early_stopping_rounds=20)
        # #定义参数网格，超参数搜索空间
        # param_grid = {
        #     'max_depth': [3, 5, 7],
        #     'learning_rate': [0.01, 0.1, 0.2],
        #     # 'subsample': [0.8, 1.0],
        #     # 'colsample_bytree': [0.8, 1.0]
        # }
        # #定义时间序列交叉验证，需要使用TimeSeriesSplit方法，防止数据泄露
        # cv = TimeSeriesSplit(n_splits=5) #n_splits:折数
        # grid_search = GridSearchCV(xgb,
        #                             param_grid,
        #                             cv=cv,
        #                             verbose=50)
        # #早停的验证集,在fit时传入
        # grid_search.fit(x_train, y_train,eval_set=[(x_val, y_val)])
        # print('最佳模型:', grid_search.best_estimator_)
        # print('最佳树数量:', grid_search.best_estimator_.best_iteration)

        # 3.模型实例化,模型训练(xgb网格搜索后,需要把训练集和验证集一起用最优超参数再重新训练下)
        best_xgb = XGBRegressor(n_estimators=191,max_depth=3,learning_rate=0.1)
        total_x_train = pd.concat([x_train, x_val], axis=0)
        total_y_train = pd.concat([y_train, y_val], axis=0)
        best_xgb.fit(total_x_train, total_y_train)

        # 4.模型评价
        y_pred = best_xgb.predict(x_test)
        mae = mean_absolute_error(y_test, y_pred)
        print("评估指标 MAE: ", mae)

        # 5.模型保存
        joblib.dump(best_xgb, '../model/best_xgb.pkl')

        self.logger.info("=======================模型训练完成=============================")

if __name__ == '__main__':
    load_train = PowerLoadModel('../data/train.csv')
    # load_train.ana_data()
    load_train.feature_engineering()
    # load_train.model_train()