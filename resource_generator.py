#此模块用于随机生成资源上限、已分配资源和需求资源，并计算可用资源。
import random


def generate_resources(n, m):
    # 初始化数据结构
    max_demand = []
    allocation = []
    need = []
    time = []

    # 生成每个进程的资源信息
    for i in range(n):
        max_row = []
        alloc_row = []
        need_row = []
        time_row = []

        for j in range(m):
            # 生成最大需求（1-10）
            max_val = random.randint(1, 10)
            max_row.append(max_val)

            # 生成已分配资源（0到max_val-1）
            alloc_val = random.randint(0, max_val - 1)
            alloc_row.append(alloc_val)

            # 计算需求资源
            need_row.append(max_val - alloc_val)

            # 生成时间（如果已分配资源>0则1-5，否则0）
            time_val = random.randint(1, 5) if alloc_val > 0 else 0
            time_row.append(time_val)

        max_demand.append(max_row)
        allocation.append(alloc_row)
        need.append(need_row)
        time.append(time_row)

    # 生成可用资源（1-5）
    available = [random.randint(1, 5) for _ in range(m)]

    # 计算实际总资源（已分配 + 可用）
    resource_max = [
        sum(allocation[i][j] for i in range(n)) + available[j]
        for j in range(m)
    ]

    return {
        'n': n,
        'm': m,
        'max_demand': max_demand,
        'allocation': allocation,
        'need': need,
        'available': available,
        'time': time,
        'resource_max': resource_max
    }