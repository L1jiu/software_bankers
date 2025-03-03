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
    # 引入资源权重，这里简单地将资源的索引加 1 作为权重
    resource_weights = [i + 1 for i in range(m)]
    weighted_total_allocated = 0
    weighted_available = 0
    for i in sequence:
        for j in range(m):
            work[j] += allocation[i][j]
            total_allocated[j] += allocation[i][j]
            # 计算加权的已分配资源
            weighted_total_allocated += allocation[i][j] * resource_weights[j]
    # 计算加权的可用资源
    for j in range(m):
        weighted_available += available[j] * resource_weights[j]
    # 计算加权的资源利用效率
    utilization = weighted_total_allocated / weighted_available
    return utilization