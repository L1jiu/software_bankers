#这个模块负责生成所有可能的序列，筛选出安全序列，并根据资源利用效率对安全序列进行排序。
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
    for i in sequence:
        for j in range(m):
            work[j] += allocation[i][j]
            total_allocated[j] += allocation[i][j]
    utilization = sum(total_allocated) / sum(available)
    return utilization