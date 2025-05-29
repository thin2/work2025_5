# 问题1：判断闰年
def question1():
    try:
        year = int(input("请输入年份："))
        if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
            print(f"{year}年是闰年")
        else:
            print(f"{year}年是平年")
    except ValueError:
        print("输入的不是有效的年份！")

# 问题2：生成随机数组并找最大值及索引
def question2():
    import numpy as np
    array_a = np.random.randint(-5, 6, 30)
    print("生成的随机数组：", array_a)
    max_val = -5
    max_indices = []
    i = 0
    while i < len(array_a):
        current = array_a[i]
        if current > max_val:
            max_val = current
            max_indices = [i]
        elif current == max_val:
            max_indices.append(i)
        i += 1
    print("最大值：", max_val)
    print("最大值所有索引：", max_indices)
    return array_a

# 问题3：升序和降序排序并记录原索引
def question3(array_a):

    array_S = array_a.copy()
    array_S_index = list(range(len(array_S)))
    n = len(array_S)
    for i in range(n):
        for j in range(n - i - 1):
            if array_S[j] > array_S[j + 1]:

                array_S[j], array_S[j + 1] = array_S[j + 1], array_S[j]
                array_S_index[j], array_S_index[j + 1] = array_S_index[j + 1], array_S_index[j]
    print("\n升序排序结果：", array_S)
    print("原数组索引：", array_S_index)


    array_J = array_a.copy()
    array_J_index = list(range(len(array_J)))
    for i in range(n):
        for j in range(n - i - 1):
            if array_J[j] < array_J[j + 1]:

                array_J[j], array_J[j + 1] = array_J[j + 1], array_J[j]
                array_J_index[j], array_J_index[j + 1] = array_J_index[j + 1], array_J_index[j]
    print("\n降序排序结果：", array_J)
    print("原数组索引：", array_J_index)


    print("\n原数组：", array_a)

if __name__ == "__main__":

    question1()
    array_a = question2()
    question3(array_a)