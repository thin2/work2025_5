# 导入所需的库
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# 定义数据处理和建模函数
def process_data(data):
    # 将原始数据转换为 NumPy 数组
    data = np.array(data)
    # 转置数据，使得每一列对应一个变量
    data = data.T

    # 定义列名，构建 DataFrame
    columns = ['temperature', 'pressure', 'gas_flow', 'oxygen_content']
    data = pd.DataFrame(data, columns=columns)

    # 使用标准化器对特征进行标准化（均值为0，方差为1）
    scaler = StandardScaler()
    data[['temperature', 'pressure', 'gas_flow', 'oxygen_content']] = scaler.fit_transform(
        data[['temperature', 'pressure', 'gas_flow', 'oxygen_content']]
    )

    # 将数据集分为特征（X）和目标变量（y）
    X = data[['temperature', 'pressure', 'gas_flow']]  # 输入特征
    y = data['oxygen_content']  # 输出标签（目标变量）

    # 拆分训练集和测试集，比例为 70%:30%
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 初始化并训练 XGBoost 回归模型
    model = XGBRegressor(random_state=42)
    model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = model.predict(X_test)

    # 评估模型性能：计算均方误差和R²决定系数
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 设置每个特征的报警阈值（标准化后的阈值）
    thresholds = {
        'temperature': 1.5,
        'pressure': 1.5,
        'gas_flow': 1.5,
        'oxygen_content': 1.5
    }

    # 判断是否超出阈值的函数（只要有任意一个特征超过阈值就报警）
    def check_over_temperature(row):
        return int(any(row[feature] > threshold for feature, threshold in thresholds.items()))

    # 对每一行应用报警判断逻辑，新增一列表示是否超温预警
    data['over_temperature_warning'] = data.apply(check_over_temperature, axis=1)

    # 统计所有超温预警的记录数量
    over_temperature_count = data['over_temperature_warning'].sum()

    # 构造结果字典
    result = {
        'json_data': {
            'mse(均方误差)': float(mse),
            'r2(决定系数)': float(r2),
            'over_temperature_warning(超温警告数量)': int(over_temperature_count)
        }
    }

    return result


# 从 CSV 文件中读取原始数据
from data_change.data_change import convert_csv_to_list#这个应该是其他py文件的函数
real_data = convert_csv_to_list("高炉超温报警.csv")

# 调用数据处理函数，获取分析结果
real_result = process_data(real_data)

# 打印最终结果
print(real_result)
