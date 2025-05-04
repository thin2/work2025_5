import random

class System:
    def __init__(self):
        self.problem_count = 5
        self.answer_chances = 3

    def show_menu(self):
        print("\n欢迎使用小学生算术训练系统")
        print("1. 两位数加法")
        print("2. 两位数减法")
        print("3. 两位数乘法")
        print("4. 两位数除法")
        print("5. 设置题量大小(每次训练出的题目数)")
        print("6. 设置答题机会(机会用光则公布答案)")
        print("0. 退出程序")

    def run(self):
        while True:
            self.show_menu()
            choice = input("请输入选项：")
            if choice == '1':
                self.train("addition")
            elif choice == '2':
                self.train("subtraction")
            elif choice == '3':
                self.train("multiplication")
            elif choice == '4':
                self.train("division")
            elif choice == '5':
                self.set_problem_count()
            elif choice == '6':
                self.set_answer_chances()
            elif choice == '0':
                print("退出程序，谢谢使用！")
                break
            else:
                print("无效选项，请重新输入。")

    def set_problem_count(self):
        try:
            count = int(input("请输入每次训练的题目数量："))
            if count > 0:
                self.problem_count = count
                print("题量已设置为：", self.problem_count)
            else:
                print("题目数量必须大于0。")
        except ValueError:
            print("请输入一个有效的整数。")

    def set_answer_chances(self):
        try:
            chances = int(input("请输入每道题的答题机会："))
            if chances > 0:
                self.answer_chances = chances
                print("答题机会已设置为：", self.answer_chances)
            else:
                print("答题机会必须大于0。")
        except ValueError:
            print("请输入一个有效的整数。")

    def train(self, operation):
        for i in range(1, self.problem_count + 1):

            if operation == "addition":
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                correct = a + b
                op_symbol = '+'
            elif operation == "subtraction":
                a = random.randint(10, 99)
                b = random.randint(10, a)
                correct = a - b
                op_symbol = '-'
            elif operation == "multiplication":
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                correct = a * b
                op_symbol = '*'
            elif operation == "division":
                b = random.randint(10, 99)
                quotient = random.randint(1, 9)
                a = b * quotient
                correct = quotient
                op_symbol = '/'
            else:
                return

            print(f"\n第{i}题: {a} {op_symbol} {b} = ?")
            attempts = self.answer_chances
            while attempts > 0:
                try:

                    answer = float(input("你的答案："))
                    if abs(answer - correct) < 1e-5:
                        print("回答正确！")
                        break
                    else:
                        attempts -= 1
                        if attempts > 0:
                            print(f"回答错误，请再试一次，还有{attempts}次机会。")
                        else:
                            print(f"回答错误，正确答案是: {correct}")
                except ValueError:
                    print("请输入有效的数字。")
                    continue

if __name__ == "__main__":
    system = System()
    system.run()
