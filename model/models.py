import time
from db import db_handler
from db.db_handler import Base
from conf import setting
import os
from lib import common


class OldboyPeople:

    def __init__(self, school, name, age, password):
        self.school = school
        self.name = name
        self.age = age
        self.password = password

    def logout(self):
        quit()


class Student(OldboyPeople, Base):
    kind = 'student'

    def __init__(self, school, name, age, password):
        super().__init__(school, name, age, password)
        self.have_pay = 0
        self.classes = None
        self.score = {}
        self.state = 0
        self.arr_date = []
        self.record = []
        self.homework = {'', }
        self.finish = {'', }

    def __save_teachers(self):
        for i in self.classes.teachers:
            i.dump_db()

    def __start(self):
        if self.classes:
            return True
        print('请先缴费并选择班级')

    def pay(self):  # 缴费
        if self.have_pay == 1:
            print('您已缴费')
            return
        self.have_pay = 1
        print('缴费成功')
        self.dump_db()

    def choose_class(self):  # 选择班级
        if not self.have_pay:
            print('请先缴费')
            return
        if self.classes:
            print('您选择好班级')
            return
        class_list = [(index, i.split('.')[0]) for index, i in enumerate(os.listdir(setting.CLASSES_DB))]
        while True:
            for i in class_list:
                print(i[0], i[1])
            choose = common.must_digit()
            if choose >= len(class_list):
                print('没有该班级')
                continue
            print(class_list)
            print(class_list[choose][1])
            classes = db_handler.load_db('classes', class_list[choose][1])
            self.classes = classes
            classes.students.append(self)
            self.dump_db()
            classes.dump_db()
            self.__save_teachers()
            break

    def sign(self):  # 签到
        if not self.__start():
            return
        print(self.arr_date)
        if self.arr_date:
            if time.strftime('%Y-%m-%d') != self.arr_date[-1]:
                self.state = 0
        if self.state == 0:
            sign_date = time.strftime('%Y-%m-%d')
            self.arr_date.append(sign_date)
            self.state = 1
            print('签到成功')
            if int(time.strftime('%Y-%m-%d %X').split(' ')[1].split(':')[0]) > 8:  # 8点之后签到就迟到
                print('您已迟到，请下次注意')
                info = '%s %s迟到' % (sign_date, self.name)
                self.record.append(info)
            self.dump_db()
        else:
            print('今日已签到')

    def check_homework(self):  # 查看作业
        if not self.__start():
            return
        if not self.classes.homework:
            print('还未布置作业')
            return
        for i in self.classes.homework:
            self.homework.add(i)
        print('所有作业：')
        for i in self.homework:
            print(i)
        tem = self.homework - self.finish
        if not tem:
            print('恭喜您，暂时没作业啦')
        else:
            print('未完成作业：')
            for i in tem:
                print(i)

    def finish_homework(self):  # 完成作业
        if not self.__start():
            return
        tem = self.homework - self.finish
        if not tem:
            print('您已经没有作业啦')
        else:
            while True:
                print('未完成作业：')
                for i in tem:
                    print(i)
                choose = input('请输入想要完成的作业')
                if choose not in tem:
                    print('没有该作业')
                    continue
                self.finish.add(choose)
                self.classes.finished[choose].append(self)
                self.dump_db()
                self.classes.dump_db()
                self.__save_teachers()
                break

    def check_score(self):  # 查看成绩
        if not self.__start():
            return
        if not self.score:
            print('还未有批改好的作业')
        for k, v in self.score.items():
            print(k, v)

    def check_class_info(self):  # 查看班级信息
        if not self.__start():
            return
        print('班级信息：')
        self.classes.tell_class_info()
        print('同学信息：')
        self.classes.tell_student_info()
        print('课程信息：')
        self.classes.tell_lesson_info()

    def tell_info(self):  # 查看个人信息
        if not self.__start():
            return
        info = '''
        学校：%s
        姓名：%s
        年龄：%s
        '''%(self.school,self.name,self.age)
        print(info)
        for i in self.record:
            print(i)


class Teacher(OldboyPeople, Base):
    kind = 'teacher'

    def __init__(self, school, name, age, password):
        super().__init__(school, name, age, password)
        self.classes = []

    def __choose_class(self):
        while True:
            for index, i in enumerate(self.classes):
                print(index, i.name)
            choose = common.must_digit()
            if choose >= len(self.classes):
                print('没有该班级')
                continue
            break
        return choose

    def __save_students(self):
        for i in self.classes:
            for k in i.students:
                k.dump_db()

    def homework(self):  # 发布作业
        choose = self.__choose_class()
        info = input('您输入作业内容')
        self.classes[choose].homework.append(info)
        self.classes[choose].finished[info] = []
        print('发布成功')
        self.dump_db()
        self.__save_students()
        self.classes[choose].dump_db()

    def check_stu_homework(self):  # 查看交作业情况
        choose = self.__choose_class()
        while True:
            for i in self.classes[choose].finished:
                print(i)
            work_name = input('请输入想要查看的作业名')
            if work_name not in self.classes[choose].finished:
                print('没有该作业')
                continue
            if not self.classes[choose].finished[work_name]:
                print('还没有学生交该作业')
                return
            for stu in self.classes[choose].finished[work_name]:  # 循环打印出已交作业的学生名
                print('已交作业学生名：')
                print(stu.name)
            break

    def score(self):  # 打分
        choose = self.__choose_class()
        while True:
            for i in self.classes[choose].finished:
                print(i)
            work_name = input('请输入想要批改的作业名')
            if work_name not in self.classes[choose].finished:
                print('没有该作业')
                continue
            for stu in self.classes[choose].finished[work_name]:  # 循环打印出已交作业的学生名
                print(stu.name)
            choose_stu = input('请输入想要修改的学生名')
            for stu in self.classes[choose].finished[work_name]:
                if stu.name == choose_stu:
                    while True:
                        score = input('请输入分数')
                        if not score.isdigit():
                            print('请输入整数')
                            continue
                        score = int(score)
                        stu.score[work_name] = score
                        print('打分成功')
                        self.dump_db()
                        self.classes[choose].dump_db()
                        stu.dump_db()
                        return
            else:
                print('没有该学生')

    def check_class_info(self):  # 查看班级信息
        choose = self.__choose_class()
        print('学生名单')
        self.classes[choose].tell_student_info()

    def give_lesson(self):  # 上课
        choose = self.__choose_class()
        info = input('请输入上课信息')
        self.classes[choose].lesson_record.append(info)
        self.dump_db()
        self.__save_students()
        self.classes[choose].dump_db()


class School(Base):
    kind = 'school'

    def __init__(self, name, address, city):
        self.name = name
        self.address = address
        self.city = city
        self.classes = []
        self.teachers = []
        self.courses = []

    def create_classes(self):
        while True:
            for i in self.courses:  # 选择绑定的课程
                print(i.name)
            choose = input('请输入班级所上课程')
            for i in self.courses:
                if choose == i.name:
                    course = i
                    break
            else:
                print('没有该课程')
                continue
            name = input('请输入班级名')
            for i in self.classes:
                if i.name == name:
                    print('该班级已存在')
                    break
            else:
                start_time = input('请输入开班日期')
                new_class = Classes(self.name, name, start_time, course)
                self.classes.append(new_class)
                new_class.dump_db()
                self.dump_db()
                print('创建成功')
                break

    def create_teachers(self):
        while True:
            name = input('请输入老师名字')
            for i in self.teachers:
                if i.name == name:
                    print('该老师已存在')
                    break
            else:
                password = input('请输入老师密码')
                age = input('请输入老师年龄')
                teacher = Teacher(self.name, name, age, password)
                self.teachers.append(teacher)
                teacher.dump_db()
                self.dump_db()
                print('创建成功')
                break

    def create_courses(self):
        while True:
            name = input('请输入与课程名')
            for i in self.courses:
                if i.name == name:
                    print('已有该课程')
                    break
            else:
                period = input('请输入课程周期')
                price = input('请输入课程价格')
                course = Courses(name, period, price)
                self.courses.append(course)
                self.dump_db()
                course.dump_db()
                print('创建成功')
                break

    def teacher_classes(self):
        while True:
            for i in self.classes:  # 选择绑定的班级
                print(i.name)
            choose = input('请需要绑定老师的班级')
            for i in self.classes:
                if choose == i.name:
                    classes = i
                    break
            else:
                print('没有该班级')
                continue
            for i in self.teachers:  # 选择绑定的班级
                print(i.name)
            choose = input('请需要绑定的老师')
            for i in self.teachers:
                if choose == i.name:
                    teacher = i
                    break
            else:
                print('没有该老师')
                continue
            teacher.classes.append(classes)
            classes.teachers.append(teacher)
            teacher.dump_db()
            classes.dump_db()
            self.dump_db()
            print('绑定成功')
            break

    def classes_info(self):
        for i in self.classes:
            print(i.name)

    def courses_info(self):
        for i in self.courses:
            print(i.name)

    def teachers_info(self):
        for i in self.teachers:
            print(i.name)

    def logout(self):
        quit()


class Classes(Base):
    kind = 'classes'

    def __init__(self, school, name, start_date, course):
        self.school = school
        self.name = name
        self.start_date = start_date
        self.courses = course
        self.teachers = []
        self.students = []
        self.lesson_record = []
        self.homework = []
        self.finished = {}

    def tell_class_info(self):
        print(self.school, self.name, self.start_date, self.courses.name)
        print('教师有：')
        for i in self.teachers:
            print(i.name)

    def tell_student_info(self):
        for i in self.students:
            print(i.name)

    def tell_lesson_info(self):
        for i in self.lesson_record:
            print(i)

    def check_homework(self):
        for i in self.homework:
            print(i)

    def check_finished(self):
        while True:
            for i in self.finished:
                print(i)
            choose = input('请输入作业名')
            if choose not in self.finished:
                print('没有该作业名')
                continue
            for i in self.finished[choose]:
                print(i.name)


class Courses(Base):
    kind = 'course'

    def __init__(self, name, period, price):
        self.name = name
        self.period = period
        self.price = price

    def tell_info(self):
        print('name:%s'
              'period:%s'
              'price:%s' % (self.name, self.period, self.price))
