n,m=map(int,input().split())
board=[list(input()) for i in range(n)]
# print
def check(x,y):
    for r in range(max(0,x-1),min(n,x+2)):
        for c in range(max(0,y-1),min(m,y+2)):
            if board[r][c]=='m':
                return False
    return True

pro=[]
no=[]
for i in range(n):
    for j in range(m):
        if board[i][j]=='w':
            if check(i,j):
                for r in range(max(0,i-1),min(n,i+2)):
                    for c in range(max(0,j-1),min(m,j+2)):
                        if board[r][c]=='.':
                            pro.append([r,c])
        elif board[i][j]=='c':
            for r in range(max(0, i - 1), min(n, i + 2)):
                for c in range(max(0, j - 1), min(m, j + 2)):
                    if board[r][c] == '.':
                        no.append([r, c])
count=0
for point in pro:
    if point in no:
        pass
    else:
        print(point[0]+1,point[1]+1)
        count+=1
if count==0:
    print("Too cold!")

# n, m = map(int, input().split())
# board = [list(input().strip()) for _ in range(n)]
#
# def get_3x3_coords(x, y):
#     """生成有效3x3区域的坐标"""
#     for r in range(max(0, x-1), min(n, x+2)):
#         for c in range(max(0, y-1), min(m, y+2)):
#             yield (r, c)
#
# # 使用集合自动去重并提升查询效率
# candidates = set()
# forbidden = set()
#
# for i in range(n):
#     for j in range(m):
#         if board[i][j] == 'w':
#             # 检查3x3范围内是否有'm'
#             if all(board[r][c] != 'm' for r, c in get_3x3_coords(i, j)):
#                 # 收集可候选的点
#                 for r, c in get_3x3_coords(i, j):
#                     if board[r][c] == '.':
#                         candidates.add((r, c))
#         elif board[i][j] == 'c':
#             # 收集禁止的点
#             for r, c in get_3x3_coords(i, j):
#                 if board[r][c] == '.':
#                     forbidden.add((r, c))
#
# result = candidates - forbidden
#
# if result:
#     for r, c in sorted(result):
#         print(r+1, c+1)
# else:
#     print("Too cold!")
