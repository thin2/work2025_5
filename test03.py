import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

def create_app():
    root = tk.Tk()
    root.title("学生成绩曲线图")
    root.geometry("600x600")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="学生姓名：").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(input_frame, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="请输入最近10次成绩（用逗号或空格隔开）：").grid(row=1, column=0, columnspan=2, pady=10)
    score_text = tk.Text(input_frame, height=3, width=40)
    score_text.grid(row=2, column=0, columnspan=2)

    chart_frame = tk.Frame(root)
    chart_frame.pack(pady=20, fill="both", expand=True)

    canvas_widget = None

    def draw_chart():
        nonlocal canvas_widget
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入学生姓名")
            return

        raw_input = score_text.get("1.0", tk.END).strip()

        parts = raw_input.replace(",", " ").split()
        try:
            scores = [float(x) for x in parts]
            if len(scores) != 10:
                raise ValueError("成绩数量不足10个")
        except ValueError:
            messagebox.showerror("错误", "请输入10个有效成绩，用空格或逗号隔开")
            return

        if canvas_widget:
            canvas_widget.get_tk_widget().destroy()

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(range(1, 11), scores, marker='o', linestyle='-', color='blue')
        ax.set_title(f"{name} 的最近10次成绩曲线图")
        ax.set_xlabel("考试次数")
        ax.set_ylabel("成绩")
        ax.set_ylim(0, 100)
        ax.grid(True)

        canvas_widget = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack()

    def clear_inputs():
        name_entry.delete(0, tk.END)
        score_text.delete("1.0", tk.END)
        if canvas_widget:
            canvas_widget.get_tk_widget().destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="生成图表", command=draw_chart).pack(side="left", padx=10)
    tk.Button(button_frame, text="清空输入", command=clear_inputs).pack(side="left", padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()
