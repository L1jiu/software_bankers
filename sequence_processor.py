# 这个模块负责生成所有可能的序列，筛选出安全序列，并根据资源利用效率对安全序列进行排序。
import itertools

def generate_all_sequences(n):
    return itertools.permutations(range(n))

def calculate_resource_utilization(state, sequence):
    n = state['n']
    m = state['m']
    available = state['available']
    allocation = state['allocation']
    need = state['need']
    work = available.copy()
    total_allocated = [0] * m

    # 用于记录每个进程的等待时间
    waiting_times = [0] * n
    # 记录总等待时间
    total_waiting_time = 0

    # 模拟资源分配过程
    for idx, i in enumerate(sequence):
        # 计算当前进程的等待时间
        waiting_time = sum([max(0, need[i][j] - work[j]) for j in range(m)])
        waiting_times[i] = waiting_time
        total_waiting_time += waiting_time

        for j in range(m):
            work[j] += allocation[i][j]
            total_allocated[j] += allocation[i][j]

    # 计算平均等待时间
    average_waiting_time = total_waiting_time / n if n > 0 else 0

    # 计算资源周转率（假设每个进程的执行时间为 1 单位时间）
    resource_turnover_rate = n / average_waiting_time if average_waiting_time != 0 else 0

    # 计算资源闲置率
    total_resource_time = sum([sum(allocation[i]) for i in range(n)])
    total_available_time = sum([available[j] * len(sequence) for j in range(m)])
    resource_idle_rate = (total_available_time - total_resource_time) / total_available_time if total_available_time != 0 else 0

    # 归一化处理，避免分母为 0
    normalized_waiting_time = 1 / (average_waiting_time + 1e-9) if average_waiting_time != 0 else 0
    normalized_turnover_rate = resource_turnover_rate
    normalized_idle_rate = 1 - resource_idle_rate

    # 计算资源利用效率，考虑平均等待时间、资源周转率和闲置资源率
    # 采用更复杂的加权求和，避免精度丢失
    total_normalized = normalized_waiting_time + normalized_turnover_rate + normalized_idle_rate
    if total_normalized == 0:
        utilization = 0
    else:
        utilization = (normalized_waiting_time + normalized_turnover_rate + normalized_idle_rate) / 3

    return utilization