import tkinter as tk
from tkinter import messagebox

def custom_encrypt(key: int, const_a: int, const_b: int) -> str:
    encrypted = (key * const_a + const_b) % 100000000
    encrypted_str = f"{encrypted:08d}"
    return encrypted_str[:6]

def encrypt():
    try:
        key = int(entry_key.get())
        const_a = int(entry_const_a.get())
        const_b = int(entry_const_b.get())
    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数")
        return

    encrypted = custom_encrypt(key, const_a, const_b)
    result_label.config(text=f"加密结果：{encrypted}")

# 创建主窗口
root = tk.Tk()
root.title("加密器")
root.geometry("320x280")

# 密钥输入
tk.Label(root, text="请输入数字密钥 (key):").pack(pady=5)
entry_key = tk.Entry(root)
entry_key.pack()

# const_a 输入
tk.Label(root, text="请输入乘数常量 (const_a):").pack(pady=5)
entry_const_a = tk.Entry(root)
entry_const_a.insert(0, "172391")  # 默认值
entry_const_a.pack()

# const_b 输入
tk.Label(root, text="请输入加数常量 (const_b):").pack(pady=5)
entry_const_b = tk.Entry(root)
entry_const_b.insert(0, "271828")  # 默认值
entry_const_b.pack()

# 加密按钮
tk.Button(root, text="加密", command=encrypt).pack(pady=10)

# 显示结果
result_label = tk.Label(root, text="加密结果：")
result_label.pack(pady=10)

# 启动事件循环
root.mainloop()
