#该模块负责创建图形用户界面，处理用户输入，并显示算法运行结果

import tkinter as tk
from tkinter import messagebox, ttk
import resource_generator
import banker_algorithm
import sequence_processor
import sv_ttk

def run_banker_algorithm():
    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
        state = resource_generator.generate_resources(n, m)
        result_info_text.delete('1.0', tk.END)

        # 清空之前的表格数据
        for item in resource_table.get_children():
            resource_table.delete(item)
        for item in allocation_table.get_children():
            allocation_table.delete(item)
        for item in need_table.get_children():
            need_table.delete(item)

        # 插入资源上限和可用资源到表格
        resource_table.insert("", "end", values=("资源上限", *state['resource_max']))
        resource_table.insert("", "end", values=("可用资源", *state['available']))

        # 插入已分配资源到表格
        for i in range(n):
            allocation_table.insert("", "end", values=(f"客户 {i}", *state['allocation'][i]))

        # 插入需求资源到表格
        for i in range(n):
            need_table.insert("", "end", values=(f"客户 {i}", *state['need'][i]))

        all_sequences = sequence_processor.generate_all_sequences(n)
        safe_sequences = []
        for sequence in all_sequences:
            is_safe_flag, _ = banker_algorithm.is_safe({
                'n': n,
                'm': m,
                'available': state['available'].copy(),
                'allocation': state['allocation'],
                'need': state['need']
            })
            if is_safe_flag:
                utilization = sequence_processor.calculate_resource_utilization(state, sequence)
                safe_sequences.append((sequence, utilization))
        safe_sequences.sort(key=lambda x: x[1], reverse=True)

        result_text = "安全序列及资源利用效率：\n"
        for sequence, utilization in safe_sequences:
            result_text += f"序列: {sequence}, 资源利用效率: {utilization:.2f}\n"

        result_info_text.insert(tk.END, result_text)

    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数！")


def create_gui():
    global entry_n, entry_m, resource_table, allocation_table, need_table, result_info_text
    root = tk.Tk()
    root.title("银行家算法模拟")

    # 用户输入部分
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10)

    label_n = ttk.Label(input_frame, text="客户数量 (n):")
    label_n.pack(side=tk.LEFT, padx=5)
    entry_n = ttk.Entry(input_frame)
    entry_n.pack(side=tk.LEFT, padx=5)

    label_m = ttk.Label(input_frame, text="资源类型数量 (m):")
    label_m.pack(side=tk.LEFT, padx=5)
    entry_m = ttk.Entry(input_frame)
    entry_m.pack(side=tk.LEFT, padx=5)

    button_run = ttk.Button(root, text="运行算法", command=run_banker_algorithm)
    button_run.pack(pady=10)

    # 资源信息显示部分
    resource_frame = ttk.Frame(root)
    resource_frame.pack(pady=10)

    # 资源上限和可用资源表格
    resource_table = ttk.Treeview(resource_frame, columns=[f"col{i}" for i in range(10)], show="headings")
    resource_table.pack(side=tk.LEFT, padx=5)
    for i in range(10):
        resource_table.heading(f"col{i}", text=f"资源 {i}" if i > 0 else "资源类型")
        resource_table.column(f"col{i}", width=80)

    # 已分配资源表格
    allocation_table = ttk.Treeview(resource_frame, columns=[f"col{i}" for i in range(10)], show="headings")
    allocation_table.pack(side=tk.LEFT, padx=5)
    allocation_table.heading("col0", text="客户")
    for i in range(1, 10):
        allocation_table.heading(f"col{i}", text=f"资源 {i}")
        allocation_table.column(f"col{i}", width=80)

    # 需求资源表格
    need_table = ttk.Treeview(resource_frame, columns=[f"col{i}" for i in range(10)], show="headings")
    need_table.pack(side=tk.LEFT, padx=5)
    need_table.heading("col0", text="客户")
    for i in range(1, 10):
        need_table.heading(f"col{i}", text=f"资源 {i}")
        need_table.column(f"col{i}", width=80)

    # 结果信息显示部分
    result_info_text = tk.Text(root, height=15, width=50)
    result_info_text.pack(pady=10)
    sv_ttk.set_theme("dark")
    root.mainloop()



if __name__ == "__main__":
    create_gui()