# 该模块负责创建图形用户界面，处理用户输入，并显示算法运行结果
import tkinter as tk
from tkinter import messagebox, ttk
import resource_generator
import banker_algorithm
import sequence_processor
import sv_ttk
from tkinter import font as tkfont
from resource_generator import generate_resources
from sequence_processor import generate_all_sequences
from banker_algorithm import is_safe
from sequence_processor import calculate_resource_utilization


# 定义全局变量
no_safe_sequence_label = None
entry_n = None
entry_m = None
resource_max_frame = None
allocation_frame = None
need_frame = None
available_frame = None
result_frame = None
root = None
input_frame = None  # 新增全局变量定义

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
        state = generate_resources(n, m)

        # 显示资源上限
        column_names = [str(j + 1) for j in range(m)]
        resource_max_table['columns'] = tuple(column_names)
        # 为动态生成的列名设置表头文本
        for col in column_names:
            resource_max_table.heading(col, text=col)
            resource_max_table.column(col, width=40)
        resource_max_table.heading('#0', text='资源上限')
        resource_max_table.insert('', tk.END, text='', values=state['resource_max'])


        # 显示已分配资源
        allocation_table['columns'] = tuple(column_names)
        # 为动态生成的列名设置表头文本
        for col in column_names:
            allocation_table.heading(col, text=col)
            allocation_table.column(col, width=20)
        allocation_table.heading('#0', text='已分配资源')
        for i in range(n):
            allocation_table.insert('', tk.END, text=f"客户 {i}", values=state['allocation'][i])

        # 显示需求资源
        need_table['columns'] = tuple(column_names)
        # 为动态生成的列名设置表头文本
        for col in column_names:
            need_table.heading(col, text=col)
            need_table.column(col, width=20)
        need_table.heading('#0', text='需求资源')
        for i in range(n):
            need_table.insert('', tk.END, text=f"客户 {i}", values=state['need'][i])

        # 显示可用资源
        available_table['columns'] = tuple(column_names)
        # 为动态生成的列名设置表头文本
        for col in column_names:
            available_table.heading(col, text=col)
            available_table.column(col, width=20)
        available_table.heading('#0', text='可用资源')
        available_table.insert('', tk.END, text='', values=state['available'])

        all_sequences = generate_all_sequences(n)
        safe_sequences = []
        for sequence in all_sequences:
            is_safe_flag, _ = is_safe({
                'n': n,
                'm': m,
                'available': state['available'].copy(),
                'allocation': state['allocation'],
                'need': state['need']
            })
            if is_safe_flag:
                utilization = calculate_resource_utilization(state, sequence)
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
            # 定义一个较大的字体
            large_font = tkfont.Font(size=16)  # 调整这里的size值以改变字体大小

            if no_safe_sequence_label is None:
                # 创建并显示标签，同时应用新的字体
                no_safe_sequence_label = tk.Label(root, text="无安全序列", font=large_font)
                no_safe_sequence_label.pack(pady=10)
            else:
                # 如果标签已存在，仅重新显示（如果之前被隐藏）
                no_safe_sequence_label.pack(pady=10)
        else:
            if no_safe_sequence_label is not None:
                # 隐藏“无安全序列”标签
                no_safe_sequence_label.pack_forget()

            # 插入数据到结果表格
            for sequence, utilization in safe_sequences:
                result_table.insert('', tk.END, values=(sequence, f"{utilization:.2f}"))

    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数！")

def create_gui():
    global entry_n, entry_m, resource_max_table, allocation_table, need_table, available_table, result_table, root, input_frame, resource_max_frame, allocation_frame, need_frame, available_frame, result_frame
    root = tk.Tk()
    root.title("银行家算法模拟")

    # 获取屏幕分辨率
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算合适的窗口大小，例如设置为屏幕宽度和高度的80%
    window_width = int(screen_width * 0.4)
    window_height = int(screen_height * 0.8)

    # 设置窗口初始大小
    root.geometry(f"{window_width}x{window_height}")

    # 创建一个主框架
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    input_frame = ttk.Frame(main_frame)
    input_frame.place(relx=0, rely=0, relwidth=1, height=30)

    # 第一列的输入框和标签
    label_n = ttk.Label(input_frame, text="客户数量 (n):")
    label_n.place(relx=0, rely=0, relwidth=0.2)
    entry_n = ttk.Entry(input_frame)
    entry_n.place(relx=0, rely=0.5, relwidth=0.2)

    # 第二列的输入框和标签
    label_m = ttk.Label(input_frame, text="资源类型数量 (m):")
    label_m.place(relx=0.2, rely=0, relwidth=0.2)
    entry_m = ttk.Entry(input_frame)
    entry_m.place(relx=0.2, rely=0.5, relwidth=0.2)

    button_run = ttk.Button(input_frame, text="运行算法", command=run_banker_algorithm)
    button_run.place(relx=0.4, rely=0.5, relwidth=0.2)

    resource_max_frame = ttk.Frame(main_frame)
    resource_max_frame.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.3)
    resource_max_label = ttk.Label(resource_max_frame, text="资源上限表格")
    resource_max_label.pack(pady=5)
    resource_max_table = ttk.Treeview(resource_max_frame, show='headings')
    resource_max_table.pack(pady=10, fill=tk.BOTH, expand=True)

    # 添加滚动条
    resource_max_scrollbar = ttk.Scrollbar(resource_max_frame, orient=tk.VERTICAL, command=resource_max_table.yview)
    resource_max_table.configure(yscrollcommand=resource_max_scrollbar.set)
    resource_max_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    allocation_frame = ttk.Frame(main_frame)
    allocation_frame.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.3)
    allocation_label = ttk.Label(allocation_frame, text="已分配资源表格")
    allocation_label.pack(pady=5)
    allocation_table = ttk.Treeview(allocation_frame, show='headings')
    allocation_table.pack(pady=10, fill=tk.BOTH, expand=True)

    # 添加滚动条
    allocation_scrollbar = ttk.Scrollbar(allocation_frame, orient=tk.VERTICAL, command=allocation_table.yview)
    allocation_table.configure(yscrollcommand=allocation_scrollbar.set)
    allocation_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    need_frame = ttk.Frame(main_frame)
    need_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.3)
    need_label = ttk.Label(need_frame, text="需求资源表格")
    need_label.pack(pady=5)
    need_table = ttk.Treeview(need_frame, show='headings')
    need_table.pack(pady=10, fill=tk.BOTH, expand=True)

    # 添加滚动条
    need_scrollbar = ttk.Scrollbar(need_frame, orient=tk.VERTICAL, command=need_table.yview)
    need_table.configure(yscrollcommand=need_scrollbar.set)
    need_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    available_frame = ttk.Frame(main_frame)
    available_frame.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.3)
    available_label = ttk.Label(available_frame, text="可用资源表格")
    available_label.pack(pady=5)
    available_table = ttk.Treeview(available_frame, show='headings')
    available_table.pack(pady=10, fill=tk.BOTH, expand=True)

    # 添加滚动条
    available_scrollbar = ttk.Scrollbar(available_frame, orient=tk.VERTICAL, command=available_table.yview)
    available_table.configure(yscrollcommand=available_scrollbar.set)
    available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_frame = ttk.Frame(main_frame)
    result_frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)
    result_label = ttk.Label(result_frame, text="结果信息表格")
    result_label.pack(pady=5)
    result_table = ttk.Treeview(result_frame, columns=('Sequence', 'Utilization'), show='headings')
    result_table.pack(pady=10, fill=tk.BOTH, expand=True)

    # 添加滚动条
    result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_table.yview)
    result_table.configure(yscrollcommand=result_scrollbar.set)
    result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    sv_ttk.set_theme("dark")

    # 绑定窗口大小改变事件
    root.bind("<Configure>", on_window_resize)

    root.mainloop()

def on_window_resize(event):
    # 重新计算并设置各个控件的位置和大小
    width = event.width
    height = event.height

    input_frame.place(relx=0, rely=0, relwidth=1, height=70)

    resource_max_frame.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.3)
    allocation_frame.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.3)
    need_frame.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.3)
    available_frame.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.3)
    result_frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3)


if __name__ == "__main__":
    create_gui()