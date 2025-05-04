import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# 数据
categories = ['数据跨境流动', '数字产品待遇', '数字服务税']
years = ['2021', '2023', '2024']
data = {
    '数据跨境流动': 1,
    '数字产品待遇': 1,
    '数字服务税': 1
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
bars = []
for i, category in enumerate(categories):
    bar = ax.bar(category, data[category], color=['#4CAF50', '#2196F3', '#FFC107'][i])
    bars.append(bar)

# 设置标题和标签
ax.set_title('美加数字贸易争议', fontsize=14, fontweight='bold')
ax.set_ylabel('争议数量', fontsize=12)

# 添加图例
ax.legend(['争议数量'], loc='upper left')

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig('美加数字贸易争议.png', dpi=300, bbox_inches='tight')

# 显示图表
plt.show()