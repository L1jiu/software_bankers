# 该模块实现银行家算法的核心逻辑，用于判断系统是否安全，并找出安全序列。
import sequence_processor

def is_safe(state):
    n = state['n']
    m = state['m']
    available = state['available']
    allocation = state['allocation']
    need = state['need']
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
        if not found:
            break
    return all(finish), safe_sequence