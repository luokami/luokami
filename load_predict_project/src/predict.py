"""
预测模块
"""
import os
import pandas as pd
import datetime

from utils.log import Logger
from utils.common import data_preprocessing
from sklearn.metrics import mean_absolute_error
import joblib
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 15
pd.set_option('display.max_columns', None)

# 预测类
class PowerLoadPredict(object):

    def __init__(self, base_path):
        # 初始化日志
        log_file = "predict_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.logger = Logger(base_path, log_file).get_logger()
        # 加载测试数据
        # os.path.join使用/拼接路径
        self.source_data = data_preprocessing(os.path.join(base_path, "data/test.csv"))
        # 初始化time_key_load字典
        self.time_key_load = self.source_data.set_index('time')['power_load'].to_dict()
        # 加载训练好的模型
        self.model = joblib.load(os.path.join(base_path, "model/best_xgb.pkl"))
        self.logger.info("================预测类初始化完成==================")

    # 构造和训练集相同格式的特征
    def pred_feature_extract(self, time_key, time_key_load=None):
        self.logger.info(f"==================开始解析{time_key}预测数据特征==================")
        # 预测数据解析特征，保持与模型训练时的特征列名一致
        # 1. 解析时间特征
        if isinstance(time_key, str):
            time_key = pd.to_datetime(time_key)

        # 添加hour和month特征
        hour= time_key.hour
        month= time_key.month
        # 把单列hour和month特征转为onehot类型
        # 初始化hour和month列表
        hour_list = [0] * 24
        month_list = [0] * 12
        # 把对应时间位置的值, 设为1
        hour_list[hour] = 1
        month_list[month - 1] = 1

        # 2. 解析时间窗口的 负荷特征
        # 这里有两种情况, 一种是offline(回测)测试, 需要对未来time_key_load进行掩码, 需要单独传进来
        # 如果是online(实时)测试, 则不需要传入time_key_load, 默认使用self.time_key_load
        time_key_load = time_key_load if time_key_load else self.time_key_load
        # 获取last_n_hour_load, 如果不存在, 则返回500负荷(之前绘图看到的中位数(近似))
        last_1_hour_load = time_key_load.get(time_key - pd.Timedelta(hours=1), 500)
        last_2_hour_load = time_key_load.get(time_key - pd.Timedelta(hours=2), 500)
        last_3_hour_load = time_key_load.get(time_key - pd.Timedelta(hours=3), 500)

        # 3. 解析昨日同时刻 负荷特征
        # 获取last_n_day_load, 如果不存在, 则返回500 负荷(之前绘图看到的中位数(近似))
        last_1_day_load = time_key_load.get(time_key - pd.Timedelta(days=1), 500)

        # 4. 构造成pandas的DataFrame
        featrue_columns =  ['前1小时', '前2小时', '前3小时', 'yesterday_load', 'hour_0', 'hour_1', 'hour_2', 'hour_3',
                            'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10', 'hour_11',
                            'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19',
                            'hour_20', 'hour_21', 'hour_22', 'hour_23', 'month_1', 'month_2', 'month_3', 'month_4',
                            'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11', 'month_12']

        featrue_list = [last_1_hour_load, last_2_hour_load, last_3_hour_load, last_1_day_load, *hour_list, *month_list]

        self.logger.info(f"==================结束解析{time_key}预测数据特征==================")
        return pd.DataFrame([featrue_list], columns=featrue_columns)

    def model_predict(self, time_key=None):
        # 模型预测同时支持在线预测和离线预测
        if time_key is not None:
            self.logger.info(f"==================(online)开始在线预测{time_key}负荷==================")
            # 解析特征
            pred_feature = self.pred_feature_extract(time_key)
            # 模型预测
            pred = self.model.predict(pred_feature)
            # print(pred[0])
            self.logger.info(f"==================(online)在线预测{time_key}负荷: {pred[0]}==================")
            self.logger.info(f"==================(online)结束在线预测{time_key}负荷==================")
            return pred[0]
        else:
            self.logger.info("=============(offline)开始离线预测(回测)==================")
            # 4.1 确定要预测的时间段（2015-08-01 00:00:00及以后的时间）
            data = self.source_data.copy()
            data = data[data.time > '2015-08-01 00:00:00']
            # 4.2 为了模拟实际场景的预测，把要预测的时间以及以后的负荷都掩盖掉，因此新建一个数据字典，只保存预测时间以前的数据字典
            # 初始化评估数据列表
            eval_list = []
            for time_key in data.time:
                # 4.3 掩盖当前时间之后的所有负荷数据
                time_key_load = {k: v for k, v in self.time_key_load.items() if k < time_key}
                pred_feature = self.pred_feature_extract(time_key, time_key_load)
                pred = self.model.predict(pred_feature)
                # 4.4 结果保存到evaluate_list，三个元素分别是预测时间、真实负荷、预测负荷，方便后续进行预测结果评价
                eval_list.append([time_key, self.time_key_load[time_key], pred[0]])

            # 4.5 循环结束后，evaluate_list转为DataFrame
            eval_df = pd.DataFrame(eval_list, columns=['当前时间', '真实负荷', '预测负荷'])

            # 4.6 评估模型
            mae = mean_absolute_error(eval_df['真实负荷'], eval_df['预测负荷'])
            print(f"评估指标 MAE: {mae}")

            # 4.7 可视化结果
            self.eval_plot(eval_df)
            self.logger.info(f"=============(offline)离线预测(回测)评估MAE指标: {mae}==================")
            self.logger.info("============= (offline)结束离线预测(回测)==================")

            return eval_df

    def eval_plot(self, eval_df):
        # 绘制实际负荷和预测负荷对比图
        plt.figure(figsize=(20, 10))
        plt.plot(eval_df['当前时间'], eval_df['真实负荷'], label='真实负荷')
        plt.plot(eval_df['当前时间'], eval_df['预测负荷'], label='预测负荷')
        plt.xlabel('时间')
        plt.ylabel('负荷')
        plt.title('实际负荷和预测负荷对比图')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    plp = PowerLoadPredict('../')
    # df = plp.pred_feature_extract('2015-08-01')
    # print(df)
    # plp.model_predict('2015-09-01')
    plp.model_predict()









