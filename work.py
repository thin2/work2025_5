
courses = [
    ['101', 'python程序设计', '公选课', '计算机学院', '2'],
    ['102', 'c++程序设计', '公选课', '计算机学院', '2']
]

def dispCourses(lst=[]):
    print('=' * 83)
    headers = ['课程编号', '课程名称', '课程类型', '开课单位', '开课学期']
    print('|'.join(header.ljust(13) for header in headers)+'|')
    print('=' * 83)
    for course in lst:
        print('|'.join(item.ljust(13) for item in course)+'|')
    print('=' * 83)
    print(f"共{len(lst)}条记录。")
    print("请输入操作码：1.添加课程 2.修改课程 3.删除课程 4.课程排序 0.退出")


def isCourseExist(courseNo):
    for idx, course in enumerate(courses):
        if course[0] == courseNo:
            return idx
    return None


def addCourse():
    n = int(input("输入课程数量："))
    print("输入课程信息（用英文逗号分开，一门课程一行）：课程号,课程名称,课程类型,开课专业,开课学期")
    count = 0
    for _ in range(n):
        info = input().strip().split(',')
        if len(info) != 5:
            continue
        course_no = info[0].strip()
        if isCourseExist(course_no) is not None:
            print(f"《{course_no}.{info[1]}》已存在，无需重复添加！")
            continue
        courses.append([item.strip() for item in info])
        count += 1
    print(f"成功添加{count}条课程信息。")

def modiCourse():
    course_no = input("输入要修改的课程号：").strip()
    idx = isCourseExist(course_no)
    if idx is None:
        print(f"编号为{course_no}的课程信息不存在，修改失败。")
        return
    new_info = input("输入该课程的新信息（用英文逗号分开）：课程号,课程名称,课程类型,开课专业,开课学期\n").strip().split(',')
    if new_info[0] != course_no:
        print("课程号不允许修改，修改失败！")
        return
    courses[idx] = [item.strip() for item in new_info]
    print("修改课程信息成功。")

def delCourse():
    course_no = input("输入要删除的课程号：").strip()
    idx = isCourseExist(course_no)
    if idx is None:
        print(f"编号为{course_no}的课程信息不存在，删除失败。")
        return
    confirm = input(f"即将删除编号为{course_no}的课程信息，确认请输入'yes'。\n").strip()
    if confirm.lower() == 'yes':
        del courses[idx]
    else:
        print("已放弃删除操作，数据未作任何修改。")

def sortCourse():
    field_map = {
        1: 0, 2: 1, 3: 2, 4: 3, 5: 4
    }
    field = int(input("输入排序的字段号码：1.课程号 2.课程名称 3.课程类型 4.开课专业 5.开课学期\n"))
    if field not in field_map:
        print("输入的字段号码有错。")
        return
    courses.sort(key=lambda x: x[field_map[field]])
    print("排序完成。")
dispCourses(courses)
while True:
    try:
        key = int(input())
    except ValueError:
        print("选择有错，请重新选择正确的功能编号。")
        continue
    if key == 1:
        addCourse()
        dispCourses(courses)
    elif key == 2:
        modiCourse()
        dispCourses(courses)
    elif key == 3:
        delCourse()
        dispCourses(courses)
    elif key == 4:
        sortCourse()
        dispCourses(courses)
    elif key == 0:
        print("退出系统成功。")
        break
    else:
        print("选择有错，请重新选择正确的功能编号。")