import math
import tabulate
import Stats


def brute_inversion(A):
    # Complete the code here, see README on course website for problem description and instructions.
    cnt = 0
    n = len(A)
    for i in range(n):
        for j in range(i+1, n):
            if A[i] > A[j]:
                cnt += 1
    Stats.Set('BruteForce_cnt', cnt)
    return cnt


cnt=0


def MERGE(A, p, q, r):
    L = A[p:q] + [float('inf')]
    R = A[q:r] + [float('inf')]
    i = j = 0

    for k in range(p, r):
        if R[j] == math.inf:
            Stats.Inc('r_inf_move_cnt')
        if L[i] <= R[j]:

            A[k] = L[i]
            i += 1
        else:
            if R[j] != float('inf'):

                Stats.Inc('inverst_cnt', len(L) - i - 1)
            else:
                Stats.Inc('r_inf_move_cnt')
            A[k] = R[j]
            j += 1



    # Complete the code here, see README on course website for problem description and instructions.




    pass
   
def MERGE_SORT(A, p, r):
    # sort subarray A[p:r]
    # e.g. to sort A[:] use MERGE_SORT(A, 0, len(A))


    if r - p > 1:
        q = (p + r) // 2
        MERGE_SORT(A, q, r)
        MERGE_SORT(A, p, q)

        MERGE(A, p, q, r)
        # Complete the code here, see README on course website for problem description and instructions.





#-------------------------------------------
# Don't change code below this line
#-------------------------------------------
def main(A):
    Stats.PrintArray(A)
    Stats.Reset()
    Stats.Set('BruteForce_cnt', brute_inversion(A))
    MERGE_SORT(A, 0, len(A))
    n = len(A)
    Stats.PrintArray(A)
    Stats.PrintStats()

    return A
if __name__ == '__main__':

    # A = [2,3,8,6,1]
    A= [18, 1, 13, 15, 18, 0, 6, 14, 15, 8]
#    A +=A

    main(A)