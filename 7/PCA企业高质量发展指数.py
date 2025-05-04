#!/usr/bin/env python
# coding: utf-8

# In[287]:


#导入数据
import pandas as pd
import numpy as np
HQD = pd.read_excel('HQD.xlsx')
HQD = HQD.drop([0])

# 提取从 A001101000 到 CO2 的列
start_column = 'A001101000'
end_column = 'CO2'

# 直接提取指定范围的列
HQD = HQD.loc[:, start_column:end_column]

# 查看提取后的数据框
HQD


# In[272]:


# 计算每列的平均值，忽略 NaN 值
column_means = HQD.mean(skipna=True)

# 将 NaN 值替换为每列的平均值
HQD.fillna(column_means, inplace=True)


# In[274]:


# 进行标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() 
scaler.fit(HQD)  
HQD2 = pd.DataFrame(scaler.transform(HQD))  
HQD2 # 查看标准化后的数据列


# In[276]:


HQD2.shape


# In[278]:


# PCA
import matplotlib.pyplot as plt  
from sklearn.decomposition import PCA  
pca = PCA(n_components=HQD2.shape[1]-1)  # 创建主成分分析对象，设定主成分数为样本特征数 - 1
reduced_x = pca.fit_transform(HQD2)  # 基于已标准化数据创建主成分分析模型
covper = pca.explained_variance_  # 降维后的各主成分的方差值
covper = pd.DataFrame(np.round(covper, 3))  

# 绘制碎石图
plt.plot(covper, 'bx--')
plt.xlabel('Component #n')
plt.ylabel('Variance')
plt.show()




# In[ ]:


coefficient=pd.DataFrame(np.round(pca.components_, 3),columns=HQD.columns)#输出载荷系数
coefficient.to_excel('HQD_coefficient.xlsx')

contribution=pd.DataFrame(np.round(pca.explained_variance_ratio_, 3) )#输出累计方差贡献率
contribution.to_excel('HQD_contribution.xlsx')


# In[284]:


pd.DataFrame(np.round(reduced_x, 3))


# In[ ]:
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# ================== 配置区域 ==================
input_file = 'HQD(1).xlsx'  # 原始数据文件
industry_col = 'Sicda_str'  # 行业分类列名（需存在于数据中）
start_column = 'A001101000'  # 数据起始列
end_column = 'CO2'  # 数据结束列
target_columns = ['A001101000', 'A001107000', 'A001110000']  # 目标分析列
output_dir = '行业分析报告'  # 输出主目录


# =============================================

def calculate_weighted_scores(data_df, weights):
    """计算加权综合得分（核心逻辑）"""
    # 验证目标列存在
    missing_cols = set(target_columns) - set(data_df.columns)
    if missing_cols:
        raise ValueError(f"缺失目标列: {missing_cols}")

    weighted_scores = (data_df[target_columns] * weights[target_columns]).sum(axis=1)

    return weighted_scores.sum()


def process_industry(group, industry_name, output_path):
    """处理单个行业分析"""
    try:
        # 创建目录
        os.makedirs(output_path, exist_ok=True)

        # 数据预处理
        numeric_df = group.drop(columns=[industry_col]).apply(pd.to_numeric, errors='coerce')
        numeric_df.fillna(numeric_df.mean(), inplace=True)

        # 标准化
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)

        # PCA分析
        pca = PCA()
        pca.fit(scaled_data)

        # 计算特征权重
        feature_weights = pd.Series(
            np.dot(pca.components_.T, pca.explained_variance_ratio_),
            index=numeric_df.columns
        )

        # 保存分析结果
        save_analysis_results(pca, numeric_df.columns, output_path)

        # 计算行业加权得分
        industry_score = calculate_weighted_scores(numeric_df, feature_weights)
        return industry_score

    except Exception as e:
        print(f"处理行业 {industry_name} 时出错: {str(e)}")
        return None


def save_analysis_results(pca, features, output_path):
    """保存分析结果"""
    # 保存载荷矩阵
    pd.DataFrame(
        pca.components_.T,
        index=features,
        columns=[f'PC{i + 1}' for i in range(pca.n_components_)]
    ).to_excel(os.path.join(output_path, '载荷矩阵.xlsx'))

    # 保存方差贡献率
    pd.DataFrame({
        '方差贡献率': pca.explained_variance_ratio_,
        '累计贡献率': np.cumsum(pca.explained_variance_ratio_)
    }).to_excel(os.path.join(output_path, '方差贡献率.xlsx'))

    # 生成碎石图
    plt.figure(figsize=(10, 6))
    plt.plot(pca.explained_variance_ratio_, 'bo-')
    plt.title('主成分方差解释率')
    plt.savefig(os.path.join(output_path, '碎石图.png'))
    plt.close()


def visualize_industry_scores(scores):
    """可视化行业得分"""
    # 准备数据
    df_scores = pd.DataFrame.from_dict(scores, orient='index', columns=['综合得分'])
    df_scores.sort_values('综合得分', ascending=False, inplace=True)

    # 绘制图表
    plt.figure(figsize=(12, 8))
    bars = df_scores['综合得分'].plot.barh(color='skyblue')

    # 装饰图表
    plt.title('行业综合得分对比', fontsize=14)
    plt.xlabel('得分', fontsize=12)
    plt.ylabel('行业', fontsize=12)
    plt.grid(axis='x', alpha=0.4)

    # 添加数据标签
    for bar in bars.containers[0]:
        width = bar.get_width()
        plt.text(width + 0.02,
                 bar.get_y() + bar.get_height() / 2,
                 f'{width:.2f}',
                 va='center')

    # 保存结果
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '行业得分对比.png'), dpi=300)
    plt.close()


def main():
    # 加载数据
    df = pd.read_excel(input_file, header=0, skiprows=[1])
    data_cols = list(df.loc[:, start_column:end_column].columns) + [industry_col]
    df = df[data_cols]

    # 按行业处理
    industry_scores = {}
    for industry, group in df.groupby(industry_col):
        dir_path = os.path.join(output_dir, str(industry))
        score = process_industry(group, industry, dir_path)
        if score is not None:
            industry_scores[industry] = score

    # 可视化结果
    if industry_scores:
        visualize_industry_scores(industry_scores)
        print(f"分析完成！结果已保存至: {os.path.abspath(output_dir)}")
    else:
        print("未生成有效得分")


if __name__ == "__main__":
    main()