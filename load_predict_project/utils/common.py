"""
数据预处理模块
    1. 包含数据加载
    2. 时间转换
    3. 时间排序
    4. 数据去重
"""
import pandas as pd


# 定义数据预处理函数
def data_preprocessing(path):
    # 1. 包含数据加载
    data = pd.read_csv(path)
    print("查看数据: ", data.head())
    data.info()

    # 2. 时间转换
    # to_datetime: 将time列str类型转换为datetime类型
    data['time'] = pd.to_datetime(data.time)
    print("查看数据: ", data.head())
    data.info()
    # 3. 时间排序
    # sort_values: 根据time列进行排序, inplace: 直接在原数据上进行排序
    data.sort_values(by='time', inplace=True)

    # 4. 数据去重
    data.drop_duplicates(inplace=True)

    return data


if __name__ == '__main__':
    data_preprocessing("../data/train.csv")