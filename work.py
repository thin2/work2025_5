# a=int(input())
# b=int(input())
# c=int(input())
# s=(a+b+c)/2
# print(f'周长={2*s:.2f}')
# print(f'面积={(s*(s-a)*(s-b)*(s-c))**0.5:.2f}')
# id=(input())
# year=id[6:10]
# month=id[10:12]
# day=id[12:14]
# if int(id[16])%2==1:
#     sex='男'
# else:
#     sex='女'
# print(f'出生：{year}年{month}月{day}日')
# print(f'性别：{sex}')
# stu_id=input()
# stu_name=input()
# print(stu_id.strip()+stu_name.strip())
# print(stu_name.strip()*3)
# my_str='纸上得来终觉浅，绝知此事要躬行'
# n=int(input())
# print(my_str[n])
# print(len(my_str))
# print(my_str.index('终'))

# num1 = float(input())
# num2 = float(input())
#
# result = num1 + num2
# result2 = num1 - num2
# result3 = num1 * num2
# result4 = num1 / num2
#
# print("{num1} + {num2} = {result:.3f}".format(num1=num1, num2=num2, result=result))
# print("{num1} - {num2} = {result2:.3f}".format(num1=num1, num2=num2, result2=result2))
# print("{num1} * {num2} = {result3:.3f}".format(num1=num1, num2=num2, result3=result3))
# print("{num1} / {num2} = {result4:.3f}".format(num1=num1, num2=num2, result4=result4))
#交换大小写
# s=input()
# print(s.swapcase())
# import math
# x=float(input())
#
# def fabs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x
# print(fabs(x))
# Begin

# End



# year = input()
# month = input()
# date = input()
#
# year_int = int(year)
# month_int = int(month)
# date_int = int(date)
#
# print(f"{year_int} {month_int:02d} {date_int:02d}")

# m = input().strip()
# n = input().strip()
#
# set_m = set(m)
# set_n = set(n)
#
# if set_m.issubset(set_n):
#     print("FOUND")
# else:
#     print("NOT FOUND")
# x=int(input())
# n=int(input())
# a=0
# b=0
# def my_fib_sum(x,n):
#     global a,b
#     for i in range(n):
#         a=a*10+x
#         b+=a
#     return b
# result=my_fib_sum(x,n)
# print('前n项和为:',result)