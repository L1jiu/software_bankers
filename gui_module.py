import tkinter as tk
from tkinter import messagebox
import resource_generator
import banker_algorithm
import sequence_processor


def run_banker_algorithm():
    try:
        n = int(entry_n.get())
        m = int(entry_m.get())
        state = resource_generator.generate_resources(n, m)

        # 显示资源上限
        resource_max_text = f"资源上限: {state['resource_max']}\n"
        resource_info_text.insert(tk.END, resource_max_text)

        # 显示已分配资源
        allocation_text = "已分配资源:\n"
        for i in range(n):
            allocation_text += f"客户 {i}: {state['allocation'][i]}\n"
        resource_info_text.insert(tk.END, allocation_text)

        # 显示需求资源
        need_text = "需求资源:\n"
        for i in range(n):
            need_text += f"客户 {i}: {state['need'][i]}\n"
        resource_info_text.insert(tk.END, need_text)

        # 显示可用资源
        available_text = f"可用资源: {state['available']}\n"
        resource_info_text.insert(tk.END, available_text)

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
    global entry_n, entry_m, resource_info_text, result_info_text
    root = tk.Tk()
    root.title("银行家算法模拟")

    # 用户输入部分
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    label_n = tk.Label(input_frame, text="客户数量 (n):")
    label_n.pack(side=tk.LEFT, padx=5)
    entry_n = tk.Entry(input_frame)
    entry_n.pack(side=tk.LEFT, padx=5)

    label_m = tk.Label(input_frame, text="资源类型数量 (m):")
    label_m.pack(side=tk.LEFT, padx=5)
    entry_m = tk.Entry(input_frame)
    entry_m.pack(side=tk.LEFT, padx=5)

    button_run = tk.Button(root, text="运行算法", command=run_banker_algorithm)
    button_run.pack(pady=10)

    # 资源信息显示部分
    resource_info_text = tk.Text(root, height=15, width=50)
    resource_info_text.pack(pady=10)

    # 结果信息显示部分
    result_info_text = tk.Text(root, height=15, width=50)
    result_info_text.pack(pady=10)

    root.mainloop()
