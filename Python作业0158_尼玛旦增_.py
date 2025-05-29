

# 第1题：九九乘法表
print("左下三角（for循环）：")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}*{i}={i*j:2}", end='  ')
    print()

print("\n左下三角（while循环）：")
i = 1
while i <= 9:
    j = 1
    while j <= i:
        print(f"{j}*{i}={i*j:2}", end='  ')
        j += 1
    print()
    i += 1

print("\n右上三角（for循环）：")
for i in range(1, 10):
    for _ in range(1, i):
        print(" " * 8, end='')

    for j in range(i, 10):
        print(f"{i}*{j}={i*j:2}", end='  ')
    print()

print("\n右上三角（while循环）：")
i = 1
while i <= 9:
    k = 1
    while k < i:
        print(" " * 8, end='')
        k += 1
    j = i
    while j <= 9:
        print(f"{i}*{j}={i*j:2}", end='  ')
        j += 1
    print()
    i += 1

# 第2题：斐波那契数列
a, b = 1, 1
fib_sequence = [a, b]
n = 2

while True:
    next_num = a + b
    if next_num > 100000000:
        fib_sequence.append(next_num)
        n += 1
        break
    fib_sequence.append(next_num)
    a, b = b, next_num
    n += 1

print("\n斐波那契数列直到超过1亿的项：")
for num in fib_sequence:
    print(num)
print(f"该项是第{n}项")

# 第3题：判断素数
from math import sqrt

num = int(input("\n请输入一个自然数："))
if num <= 1:
    print(f"{num}不是素数")
elif num == 2:
    print(f"{num}是素数")
else:
    is_prime = True
    if num % 2 == 0:
        is_prime = False
    else:
        for i in range(3, int(sqrt(num)) + 1, 2):
            if num % i == 0:
                is_prime = False
                break
    print(f"{num}是素数" if is_prime else f"{num}不是素数")