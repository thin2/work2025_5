class Customer:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name}:{self.age}"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return (self.age == other.age and self.name == other.name)
    def __gt__(self, other):
        if self.age == other.age:
            return self.name > other.name
        else:
            return self.age > other.age
    def __lt__(self, other):
        if self.age == other.age:
            return self.name < other.name
        else:
            return self.age < other.age
    def __ge__(self, other):
        return not self < other
    def __le__(self, other):
        return not self > other


# (a) 实现 Stack 类
class Stack:
    def __init__(self):
        self.items = []  # 用列表实现栈

    def clear(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, data):
        self.items.append(data)

    def pop(self):
        if self.isEmpty():
            return None
        return self.items.pop()

    def peek(self):
        if self.isEmpty():
            return None
        return self.items[-1]

    def display(self):
        # 显示栈顶在最右侧的元素排列
        print("Stack:", self.items)


# (b) 实现 StackSort 类
class StackSort:
    def __init__(self, data):
        # 定义两个栈：stack1 存放原始数据，stack2 用于排序
        self.stack1 = Stack()
        self.stack2 = Stack()
        for item in data:
            self.stack1.push(item)

    def sort(self):
        # 使用辅助栈对 stack1 中的元素进行排序，排序结果存储在 stack2 中
        while not self.stack1.isEmpty():
            temp = self.stack1.pop()
            # 当 stack2 非空且其栈顶元素大于 temp 时，移回 stack1
            while not self.stack2.isEmpty() and self.stack2.peek() > temp:
                self.stack1.push(self.stack2.pop())
            self.stack2.push(temp)

    def display(self):
        print("Stack1:", self.stack1.items)
        print("Stack2:", self.stack2.items)


if __name__ == "__main__":
    # 题目所给测试数据
    data1 = [
        Customer("Alice", 89),
        Customer("Bobby", 40),
        Customer("Calvin", 52),
        Customer("Dianna", 67),
        Customer("Evdee", 42)
    ]
    stackSort1 = StackSort(data1)
    print("Before stack sort:")
    stackSort1.display()
    stackSort1.sort()
    print("After stack sort:")
    stackSort1.display()

    # 测试只有一个元素
    data2 = [Customer("Zack", 50)]
    stackSort2 = StackSort(data2)
    print("\nTest Case 2 - Before sort:")
    stackSort2.display()
    stackSort2.sort()
    print("Test Case 2 - After sort:")
    stackSort2.display()

    # 测试多个年龄相同但名字不同的情况
    data3 = [
        Customer("Anna", 30),
        Customer("Bella", 30),
        Customer("Cara", 30)
    ]
    stackSort3 = StackSort(data3)
    print("\nTest Case 3 - Before sort:")
    stackSort3.display()
    stackSort3.sort()
    print("Test Case 3 - After sort:")
    stackSort3.display()
