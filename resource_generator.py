#此模块用于随机生成资源上限、已分配资源和需求资源，并计算可用资源。
import random

def generate_resources(n, m):
    # 随机生成资源上限
    resource_max = [random.randint(1, 10) for _ in range(m)]
    available = resource_max.copy()
    # 随机生成已分配资源和需求资源
    allocation = [[random.randint(0, min(available[j], 10)) for j in range(m)] for i in range(n)]
    need = [[random.randint(0, resource_max[j] - allocation[i][j]) for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            available[j] -= allocation[i][j]
    # 计算正确的资源上限
    resource_max_correct = [available[j] + sum([allocation[i][j] for i in range(n)]) for j in range(m)]
    state = {
        'n': n,
        'm': m,
        'available': available,
        'allocation': allocation,
        'need': need,
        # 新增资源上限的正确计算结果
        'resource_max': resource_max_correct
    }
    return state