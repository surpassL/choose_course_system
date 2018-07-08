from db import db_handler
from interface import admin_interface
from lib import common


def login(kind, name, password):
    obj = db_handler.load_db(kind, name)
    if not obj:
        print('没有该账号')
        return False
    if password == obj.password:
        print('登录成功')
        return obj
    print('密码错误')


def choose_school():
    while True:  # 选择需要操作的学校
        school_list = admin_interface.get_school_list()
        for i in school_list:
            print(i[0], i[1])
        choose_school = common.must_digit()
        if choose_school >= len(school_list):
            print('没有该学校')
            continue
        school = admin_interface.choose_school(school_list[choose_school][1])  # 传学校名给接口拿到学校对象
        break
    return school
