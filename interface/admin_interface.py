import os
from conf import setting
from db import db_handler


def get_school_list():
    school_list = [(index, i.split('.')[0]) for index, i in enumerate(os.listdir(setting.SCHOOL_DB))]
    return school_list


def choose_school(school_name):
    school = db_handler.load_db('school', school_name)
    return school


def admin_login(name, password):
    if name == 'admin' and password == 'admin':
        return True


def admin(adj, admin_info, choose):
    if hasattr(adj, admin_info[choose][1]):
        getattr(adj, admin_info[choose][1])()
    else:
        print('没有该功能')
