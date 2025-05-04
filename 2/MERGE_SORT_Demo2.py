import math, Stats

def fmt_num(n): return '%3s' % str(n)

def PrintPartArray(A, p, q, tag=''):
    formatted = []
    for i in range(len(A)):
        if p <= i < q:
            formatted.append(fmt_num(A[i]))
        elif i == p - 1:
            formatted.append(fmt_num("*"))
        elif i < p:
            formatted.append(fmt_num('-'))
        else:
            formatted.append(fmt_num(' '))
    r = ' '.join(formatted)
    r += '    ' + tag
    print(r)
    return r


def MERGE(A, p, q, r, is_final_merge=False):
    L = A[p:q] + [float('inf')]  # 左边子序列
    R = A[q:r] + [float('inf')]  # 右边子序列
    i = j = 0  # i 和 j 是两个子序列的指针

    for k in range(p, r):
        if R[j] == float('inf'):
            Stats.Inc('r_inf_move_cnt')  # 如果右边子序列元素已全部处理，记录右边部分移动的次数

        # 进行比较，统计比较次数
        if L[i] <= R[j]:
            Stats.Inc('cmpcnt', 1)  # 比较次数是剩余元素个数（L的）减去当前已处理的元素
            A[k] = L[i]
            i += 1
        else:
            if R[j] != float('inf'):
                # # 统计右子序列比较次数
                Stats.Inc('cmpcnt',  1)  # 比较次数是剩余元素个数（R的）减去当前已处理的元素
            else:
                Stats.Inc('r_inf_move_cnt')  # 如果是右边部分的元素直接移动，记录次数

            A[k] = R[j]
            j += 1

    # The above line prints the final trace after the merge operation

def MERGE_SORT(A, p, r):
    if r - p > 1:
        q = (p + r) // 2
        MERGE_SORT(A, p, q)
        MERGE_SORT(A, q, r)
        is_final_merge = (p == 0 and r == len(A))
        MERGE(A, p, q, r, is_final_merge)

def main(A):
    Stats.PrintArray(A)
    MERGE_SORT(A, 0, len(A))
    Stats.PrintArray(A)
    n = len(A)
    Stats.Set(' %s*log_2(%s)' % (n, n), n * (math.log2(n)))
    Stats.PrintStats()
    return A

if __name__ == '__main__':
    A = [1, 13, 15, 0, 6, 14, 15, 8]
    # A = [18, 1, 13, 15, 18, 0, 6, 14, 15, 8]
    main(A)
