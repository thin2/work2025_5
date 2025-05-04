# 使用Python+Matplotlib生成简历图（需安装库）
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(8.27, 11.69)) # A4尺寸
gs = GridSpec(4, 2, figure=fig)

# 添加文字模块
ax1 = fig.add_subplot(gs[0, :])
ax1.text(0.1, 0.8, "李谊 - 会计学专业", fontsize=16, weight='bold')
ax1.text(0.1, 0.6, "电话：182-3769-8997 | 邮箱：2819409114@qq.com", fontsize=10)

plt.axis('off') # 隐藏坐标轴
plt.savefig('resume.png', dpi=300) # 导出高清图