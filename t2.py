import tkinter as tk
from tkinter import filedialog, messagebox
import os

# 示例函数：你可以在这里替换为你的模型评估逻辑
def run_evaluation(pic_path, pre_path, label_path):
    # 假装我们跑了模型，返回这些值
    acc = 0.85
    miou = 0.78
    f1_scores = 0.81
    return acc, miou, f1_scores

def select_pic_path():
    path = filedialog.askdirectory()
    pic_path_var.set(path)

def select_pre_path():
    path = filedialog.askdirectory()
    pre_path_var.set(path)

def select_label_path():
    path = filedialog.askdirectory()
    label_path_var.set(path)

def run():
    pic_path = pic_path_var.get()
    pre_path = pre_path_var.get()
    label_path = label_path_var.get()

    if not all([pic_path, pre_path, label_path]):
        messagebox.showerror("错误", "请先选择所有路径")
        return

    # 执行预测逻辑
    acc, miou, f1_scores = run_evaluation(pic_path, pre_path, label_path)

    # 显示结果
    result_text.set(f"acc: {acc}\nmiou: {miou}\nf1_score: {f1_scores}")

# 创建主窗口
root = tk.Tk()
root.title("模型评估工具")

# 创建变量保存路径
pic_path_var = tk.StringVar()
pre_path_var = tk.StringVar()
label_path_var = tk.StringVar()
result_text = tk.StringVar()

# 布局
tk.Label(root, text="测试集图片路径:").grid(row=0, column=0, sticky='e')
tk.Entry(root, textvariable=pic_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="选择", command=select_pic_path).grid(row=0, column=2)

tk.Label(root, text="预测结果路径:").grid(row=1, column=0, sticky='e')
tk.Entry(root, textvariable=pre_path_var, width=50).grid(row=1, column=1)
tk.Button(root, text="选择", command=select_pre_path).grid(row=1, column=2)

tk.Label(root, text="标签路径:").grid(row=2, column=0, sticky='e')
tk.Entry(root, textvariable=label_path_var, width=50).grid(row=2, column=1)
tk.Button(root, text="选择", command=select_label_path).grid(row=2, column=2)

tk.Button(root, text="运行", command=run, width=15, bg='lightgreen').grid(row=3, column=1, pady=10)

tk.Label(root, textvariable=result_text, fg='blue', font=('Arial', 12)).grid(row=4, column=0, columnspan=3, pady=10)

# 启动主循环
root.mainloop()
