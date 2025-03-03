#该模块负责创建图形用户界面，处理用户输入，并显示算法运行结果
import tkinter as tk
from tkinter import messagebox, ttk
import resource_generator
import banker_algorithm
import sequence_processor
import sv_ttk


def run_banker_algorithm():
    try:
        # 清空文本框内容
        resource_info_text.delete('1.0', tk.END)
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
        # 根据资源利用效率进行排序
        safe_sequences.sort(key=lambda x: x[1], reverse=True)

        # 清空之前的结果显示
        for i in result_table.get_children():
            result_table.delete(i)

        # 插入表头
        result_table['columns'] = ('Sequence', 'Utilization')
        result_table.heading('Sequence', text='序列')
        result_table.heading('Utilization', text='资源利用效率')
        result_table.column('Sequence', width=200)
        result_table.column('Utilization', width=100)

        # 插入数据
        for sequence, utilization in safe_sequences:
            result_table.insert('', tk.END, values=(sequence, f"{utilization:.2f}"))

    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数！")


def create_gui():
    global entry_n, entry_m, resource_info_text, result_table
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
    resource_info_text = tk.Text(root, height=15, width=50)
    resource_info_text.pack(pady=10)

    # 结果信息显示部分
    result_table = ttk.Treeview(root, columns=('Sequence', 'Utilization'), show='headings')
    result_table.pack(pady=10)

    sv_ttk.set_theme("dark")
    root.mainloop()


if __name__ == "__main__":
    create_gui()