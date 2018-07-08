from model.models import Student


def register(school, name, age, password):
    stu = Student(school, name, age, password)
    stu.dump_db()


def student(adj,student_info,choose):
    if hasattr(adj, student_info[choose][1]):
        getattr(adj, student_info[choose][1])()
    else:
        print('没有该功能')