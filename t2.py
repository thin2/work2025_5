def count1(n, wei, counts):
    pos = set()
    pos.add(0)
    for i in range(n):
        cur_wei = wei[i]
        cur_cou = counts[i]
        temp = set()
        for w in pos:
            for k in range(1, cur_cou + 1):
                temp.add(w + k * cur_wei)
        pos.update(temp)
    return len(pos)
n = int(input())
wei = list(map(int, input().split()))
counts = list(map(int, input().split()))
print(n, wei, counts)