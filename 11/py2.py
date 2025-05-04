
students = []


def add_student():

    student = {}
    student['name'] = input("请输入学生姓名：")

    while True:
        age_input = input("请输入学生年龄：")
        try:
            student['age'] = int(age_input)
            break
        except ValueError:
            print("输入的年龄必须为整数，请重新输入。")

    student['scores'] = {}
    while True:
        subject = input("请输入科目名称（输入'q'结束）：")
        if subject.lower() == 'q':
            break
        while True:
            score_input = input(f"请输入{subject}成绩：")
            try:
                score = float(score_input)
                if 0 <= score <= 100:
                    student['scores'][subject] = score
                    break
                else:
                    print("成绩必须在0到100之间，请重新输入。")
            except ValueError:
                print("输入的成绩必须为数字，请重新输入。")

    students.append(student)
    print(f"成功添加学生 {student['name']} 的信息。")


def query_student():

    query_name = input("请输入要查询的学生姓名：")
    for student in students:
        if student['name'] == query_name:
            print(f"\n姓名: {student['name']}")
            print(f"年龄: {student['age']}")
            if student['scores']:
                print("各科成绩：")
                for subject, score in student['scores'].items():
                    print(f"  {subject}: {score}")
            else:
                print("暂无成绩信息。")
            return
    print("未找到该学生。")


def delete_student():

    del_name = input("请输入要删除的学生姓名：")
    for index, student in enumerate(students):
        if student['name'] == del_name:
            del students[index]
            print(f"成功删除学生 {del_name} 的信息。")
            return
    print("未找到该学生，无法删除。")


def modify_student():

    modify_name = input("请输入要修改信息的学生姓名：")
    for student in students:
        if student['name'] == modify_name:
            print("\n当前学生信息：")
            print(f"姓名: {student['name']}")
            print(f"年龄: {student['age']}")
            if student['scores']:
                print("各科成绩：")
                for subject, score in student['scores'].items():
                    print(f"  {subject}: {score}")
            else:
                print("暂无成绩信息。")

            new_age = input("请输入新的年龄（直接回车则保持原年龄）：")
            if new_age.strip():
                try:
                    student['age'] = int(new_age)
                except ValueError:
                    print("无效的年龄输入，保持原年龄。")

            while True:
                subject = input("请输入要修改的科目名称（输入'q'结束）：")
                if subject.lower() == 'q':
                    break
                while True:
                    new_score_input = input(f"请输入{subject}的新成绩：")
                    try:
                        new_score = float(new_score_input)
                        if 0 <= new_score <= 100:
                            student['scores'][subject] = new_score
                            break
                        else:
                            print("成绩必须在0到100之间，请重新输入。")
                    except ValueError:
                        print("输入的成绩必须为数字，请重新输入。")

            print(f"成功修改学生 {modify_name} 的信息。")
            return
    print("未找到该学生，无法修改。")


def calculate_average_score():

    query_name = input("请输入要计算平均成绩的学生姓名：")
    for student in students:
        if student['name'] == query_name:
            if not student['scores']:
                print("该学生暂无成绩信息，无法计算平均成绩。")
                return
            total_score = sum(student['scores'].values())
            num_subjects = len(student['scores'])
            avg_score = total_score / num_subjects
            print(f"{student['name']} 的平均成绩为：{avg_score:.2f}")
            return
    print("未找到该学生，无法计算平均成绩。")


def main():
    while True:
        print("\n请选择操作：")
        print("1. 添加学生信息")
        print("2. 查询学生信息")
        print("3. 删除学生信息")
        print("4. 修改学生信息")
        print("5. 计算学生平均成绩")
        print("6. 退出系统")
        choice = input("请输入你的选择：")

        if choice == "1":
            add_student()
        elif choice == "2":
            query_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            modify_student()
        elif choice == "5":
            calculate_average_score()
        elif choice == "6":
            print("感谢使用学生信息管理系统，再见！")
            break
        else:
            print("无效的选择，请重新输入。")


if __name__ == '__main__':
    main()
