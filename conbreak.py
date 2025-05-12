
result_str = []
for letter in 'Python':
    if letter == 'h':
        continue
    result_str.append(letter)
print(''.join(result_str))


result_num = []
for num in range(9, -1, -1):
    if num == 5:
        continue
    result_num.append(str(num))
print(''.join(result_num))