# 该模块负责创建图形用户界面，处理用户输入，并显示算法运行结果
import tkinter as tk
from tkinter import messagebox, ttk
import resource_generator
import banker_algorithm
import sequence_processor
import sv_ttk

# 新增全局变量 no_safe_sequence_label
no_safe_sequence_label = None

def run_banker_algorithm():
    global no_safe_sequence_label
    try:
        # 清空所有资源表格内容
        for i in resource_max_table.get_children():
            resource_max_table.delete(i)
        for i in allocation_table.get_children():
            allocation_table.delete(i)
        for i in need_table.get_children():
            need_table.delete(i)
        for i in available_table.get_children():
            available_table.delete(i)

        n = int(entry_n.get())
        m = int(entry_m.get())
        state = resource_generator.generate_resources(n, m)

        # 显示资源上限
        resource_max_table['columns'] = tuple(f"Resource {j}" for j in range(m))
        resource_max_table.heading('#0', text='资源上限')
        resource_max_table.insert('', tk.END, text='', values=state['resource_max'])

        # 显示已分配资源
        allocation_table['columns'] = tuple(f"Resource {j}" for j in range(m))
        allocation_table.heading('#0', text='已分配资源')
        for i in range(n):
            allocation_table.insert('', tk.END, text=f"客户 {i}", values=state['allocation'][i])

        # 显示需求资源
        need_table['columns'] = tuple(f"Resource {j}" for j in range(m))
        need_table.heading('#0', text='需求资源')
        for i in range(n):
            need_table.insert('', tk.END, text=f"客户 {i}", values=state['need'][i])

        # 显示可用资源
        available_table['columns'] = tuple(f"Resource {j}" for j in range(m))
        available_table.heading('#0', text='可用资源')
        available_table.insert('', tk.END, text='', values=state['available'])

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

        # 清空之前的结果显示
        for i in result_table.get_children():
            result_table.delete(i)

        # 插入表头
        result_table['columns'] = ('Sequence', 'Utilization')
        result_table.heading('Sequence', text='序列')
        result_table.heading('Utilization', text='资源利用效率')
        result_table.column('Sequence', width=200)
        result_table.column('Utilization', width=100)

        # 判断是否有安全序列
        if not safe_sequences:
            # 没有安全序列，显示“无安全序列”字样
            if no_safe_sequence_label is None:
                no_safe_sequence_label = tk.Label(root, text="无安全序列")
                no_safe_sequence_label.pack(pady=10)
            else:
                no_safe_sequence_label.pack(pady=10)
        else:
            # 有安全序列，隐藏“无安全序列”字样
            if no_safe_sequence_label is not None:
                no_safe_sequence_label.pack_forget()
            # 插入数据
            for sequence, utilization in safe_sequences:
                result_table.insert('', tk.END, values=(sequence, f"{utilization:.2f}"))

    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数！")


def create_gui():
    global entry_n, entry_m, resource_max_table, allocation_table, need_table, available_table, result_table, root
    root = tk.Tk()
    root.title("银行家算法模拟")

    # 创建一个主框架
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # 用户输入部分，放在第一行
    input_frame = ttk.Frame(main_frame)
    input_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

    label_n = ttk.Label(input_frame, text="客户数量 (n):")
    label_n.grid(row=0, column=0, padx=5)
    entry_n = ttk.Entry(input_frame)
    entry_n.grid(row=0, column=1, padx=5)

    label_m = ttk.Label(input_frame, text="资源类型数量 (m):")
    label_m.grid(row=0, column=2, padx=5)
    entry_m = ttk.Entry(input_frame)
    entry_m.grid(row=0, column=3, padx=5)

    button_run = ttk.Button(input_frame, text="运行算法", command=run_banker_algorithm)
    button_run.grid(row=0, column=4, padx=5)

    # 资源上限表格，放在第一行第二列
    resource_max_frame = ttk.Frame(main_frame)
    resource_max_frame.grid(row=1, column=1, sticky='ew')
    resource_max_label = ttk.Label(resource_max_frame, text="资源上限表格")
    resource_max_label.pack(pady=5)
    resource_max_table = ttk.Treeview(resource_max_frame, show='headings')
    resource_max_table.pack(pady=10)

    # 已分配资源表格，放在第二行第一列
    allocation_frame = ttk.Frame(main_frame)
    allocation_frame.grid(row=2, column=0, sticky='ew')
    allocation_label = ttk.Label(allocation_frame, text="已分配资源表格")
    allocation_label.pack(pady=5)
    allocation_table = ttk.Treeview(allocation_frame, show='headings')
    allocation_table.pack(pady=10)

    # 需求资源表格，放在第二行第二列
    need_frame = ttk.Frame(main_frame)
    need_frame.grid(row=2, column=1, sticky='ew')
    need_label = ttk.Label(need_frame, text="需求资源表格")
    need_label.pack(pady=5)
    need_table = ttk.Treeview(need_frame, show='headings')
    need_table.pack(pady=10)

    # 可用资源表格，放在第一行第一列
    available_frame = ttk.Frame(main_frame)
    available_frame.grid(row=1, column=0, sticky='ew')
    available_label = ttk.Label(available_frame, text="可用资源表格")
    available_label.pack(pady=5)
    available_table = ttk.Treeview(available_frame, show='headings')
    available_table.pack(pady=10)

    # 结果信息显示部分，放在第三行居中
    result_frame = ttk.Frame(main_frame)
    result_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')
    result_label = ttk.Label(result_frame, text="结果信息表格")
    result_label.pack(pady=5)
    result_table = ttk.Treeview(result_frame, columns=('Sequence', 'Utilization'), show='headings')
    result_table.pack(pady=10)

    sv_ttk.set_theme("dark")
    root.mainloop()


if __name__ == "__main__":
    create_gui()