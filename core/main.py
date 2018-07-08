from interface import admin_interface, student_interface, teacher_interface, share_interface
from lib import common


def student():
    info = '''
    0.注册
    1.登录
    2.退出'''
    while True:
        print(info)
        choose = common.must_digit()
        if choose > 2:
            print('没有该功能')
            continue
        if choose == 0:
            school = share_interface.choose_school()
            age = input('请输入您的年龄')
            name = input('请输入账号')
            password = input('请输入密码')
            student_interface.register(school.name, name, age, password)
        if choose == 1:
            name = input('请输入账号')
            password = input('请输入密码')
            adj = share_interface.login('student', name, password)
            if not adj:
                continue
            break
        if choose == 2:
            quit()
    while True:
        student_info = [
            ('缴费', 'pay'),
            ('选择班级', 'choose_class'),
            ('签到', 'sign'),
            ('查看作业', 'check_homework'),
            ('完成作业', 'finish_homework'),
            ('查看成绩', 'check_score'),
            ('查看班级信息', 'check_class_info'),
            ('查看个人信息', 'tell_info'),
            ('退出', 'logout')
        ]
        for index, i in enumerate(student_info):
            print(index, i[0])
        choose = common.must_digit()
        if choose >= len(student_info):
            print('没有该功能')
            continue
        student_interface.student(adj, student_info, choose)


def teacher():
    while True:
        name = input('请输入账号')
        password = input('请输入密码')
        adj = share_interface.login('teacher', name, password)
        if not adj:
            continue
        break
    while True:
        teacher_info = [
            ('发布作业', 'homework'),
            ('查看交作业情况', 'check_stu_homework'),
            ('打分', 'score'),
            ('查看班级信息', 'check_class_info'),
            ('上课', 'give_lesson'),
            ('退出', 'logout'),
        ]
        for index, i in enumerate(teacher_info):
            print(index, i[0])
        choose = common.must_digit()
        if choose >= len(teacher_info):
            print('没有该功能')
            continue
        teacher_interface.teacher(adj, teacher_info, choose)


def admin():
    while True:  # 管理员登录
        name = input('请输入账号')
        password = input('请输入密码')
        flag = admin_interface.admin_login(name, password)
        if flag: break
        print('账号密码错误')
    school = share_interface.choose_school()
    while True:
        admin_info = [
            ('创建讲师', 'create_teachers'),
            ('创建班级', 'create_classes'),
            ('创建课程', 'create_courses'),
            ('给班级选择老师', 'teacher_classes'),
            ('班级信息', 'classes_info'),
            ('课程信息', 'courses_info'),
            ('老师信息', 'teachers_info'),
            ('退出', 'logout'),
        ]
        for index, i in enumerate(admin_info):
            print(index, i[0])
        choose = common.must_digit()
        if choose >= len(admin_info):
            print('没有该功能')
            continue
        admin_interface.admin(school, admin_info, choose)


def run():
    func_info = '''
    1.学生视图
    2.教师视图
    3.管理员视图
    4.退出'''
    func_dic = {
        '1': student,
        '2': teacher,
        '3': admin,
        '4': quit
    }
    while True:
        print(func_info)
        choose = input('请输入序号')
        if choose in func_dic:
            func_dic[choose]()
        else:
            print('没有该功能')
