import tkinter as tk
from tkinter import messagebox, scrolledtext
from math import floor
from typing import List, Tuple, Dict, Optional
import pulp

class OptimalPipePlanner:
    def __init__(self,
                 demands: List[Tuple[int, int]],  # [(length, count), ...]
                 L_min: int,
                 L_max: int):
        self.demands = demands
        self.L_min = L_min
        self.L_max = L_max
        self.patterns = self._generate_patterns()

    def _generate_patterns(self) -> List[Dict[int, int]]:
        lengths = [d for d, _ in self.demands]
        max_counts = {d: floor(self.L_max / d) for d, _ in self.demands}
        patterns = []
        def backtrack(idx, current, used):
            if idx == len(lengths):
                if used <= self.L_max and used >= self.L_min:
                    patterns.append(current.copy())
                return
            d = lengths[idx]
            for cnt in range(max_counts[d] + 1):
                new_used = used + cnt * d
                if new_used > self.L_max:
                    break
                current[d] = cnt
                backtrack(idx + 1, current, new_used)
            current[d] = 0
        backtrack(0, {d: 0 for d in lengths}, 0)
        return [p for p in patterns if any(v > 0 for v in p.values())]

    def solve(self) -> Dict[str, Optional[Dict]]:
        prob = pulp.LpProblem('PipeCutting', pulp.LpMinimize)
        y = {i: pulp.LpVariable(f'y_{i}', lowBound=0, cat='Integer')
             for i in range(len(self.patterns))}
        prob += pulp.lpSum(y[i] for i in y)
        for d, m in self.demands:
            prob += pulp.lpSum(self.patterns[i][d] * y[i] for i in y) >= m
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if status != pulp.LpStatusOptimal:
            return {'status': pulp.LpStatus[status], 'plan': None}
        plan = []
        for i, pattern in enumerate(self.patterns):
            count = int(y[i].value())
            for _ in range(count):
                total_len = sum(d * n for d, n in pattern.items())
                plan.append({'length': total_len, 'cuts': pattern})
        return {'status': 'Optimal', 'plan': plan}

class PipeCuttingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Pipe Cutting Thinker")
        # Demand input section
        demand_frame = tk.LabelFrame(master, text="子管需求（长度-数量）")
        demand_frame.pack(padx=10, pady=5, fill='x')
        tk.Label(demand_frame, text="长度(mm)").grid(row=0, column=0, padx=5)
        tk.Label(demand_frame, text="数量").grid(row=0, column=1, padx=5)
        self.len_entries = []
        self.cnt_entries = []
        for i in range(5):  # up to 5 types
            le = tk.Entry(demand_frame, width=10)
            ce = tk.Entry(demand_frame, width=10)
            le.grid(row=i+1, column=0, padx=5, pady=2)
            ce.grid(row=i+1, column=1, padx=5, pady=2)
            self.len_entries.append(le)
            self.cnt_entries.append(ce)
        # Pipe length range
        range_frame = tk.Frame(master)
        range_frame.pack(padx=10, pady=5, fill='x')
        tk.Label(range_frame, text="原管长度范围(mm):").grid(row=0, column=0)
        self.lmin_entry = tk.Entry(range_frame, width=8)
        self.lmin_entry.grid(row=0, column=1, padx=(5,0))
        tk.Label(range_frame, text="-").grid(row=0, column=2)
        self.lmax_entry = tk.Entry(range_frame, width=8)
        self.lmax_entry.grid(row=0, column=3, padx=(0,5))
        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(padx=10, pady=5)
        tk.Button(btn_frame, text="求解", command=self.solve).pack(side='left', padx=5)
        tk.Button(btn_frame, text="清空", command=self.clear).pack(side='left', padx=5)
        # Output
        self.output = scrolledtext.ScrolledText(master, width=60, height=18)
        self.output.pack(padx=10, pady=5)

    def parse_demands(self) -> List[Tuple[int, int]]:
        demands = []
        for le, ce in zip(self.len_entries, self.cnt_entries):
            ld = le.get().strip()
            cd = ce.get().strip()
            if ld and cd:
                demands.append((int(ld), int(cd)))
        return demands

    def solve(self):
        try:
            demands = self.parse_demands()
            L_min = int(self.lmin_entry.get())
            L_max = int(self.lmax_entry.get())
            if not demands:
                raise ValueError("至少输入一行子管需求。")
        except Exception as e:
            messagebox.showerror("输入错误", f"请检查输入: {e}")
            return
        planner = OptimalPipePlanner(demands, L_min, L_max)
        result = planner.solve()
        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, f"求解状态: {result['status']}\n")
        if result['plan']:
            self.output.insert(tk.END, "具体切割方案：\n")
            for idx, item in enumerate(result['plan'], 1):
                length = item['length']
                cuts = ', '.join(f"{d}mm×{n}" for d, n in sorted(item['cuts'].items()) if n>0)
                self.output.insert(tk.END, f" 原管{idx} (长度{length}mm) 切割: {cuts}\n")
        else:
            self.output.insert(tk.END, "未找到可行方案，请调整输入。\n")

    def clear(self):
        for le, ce in zip(self.len_entries, self.cnt_entries):
            le.delete(0, tk.END)
            ce.delete(0, tk.END)
        self.lmin_entry.delete(0, tk.END)
        self.lmax_entry.delete(0, tk.END)
        self.output.delete('1.0', tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    PipeCuttingGUI(root)
    root.mainloop()
