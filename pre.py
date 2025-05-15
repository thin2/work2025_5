import tkinter as tk

root = tk.Tk()
root.title("Canvas 实践作业")
root.geometry("800x600")

def draw_shape():
    canvas.create_oval(
        400 - 100, 300 - 100, 400 + 100, 300 + 100,
        outline="yellow",
        width=5,
        fill="red"
    )

button = tk.Button(root, text="绘制图案", command=draw_shape)
button.pack(side=tk.TOP)

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
