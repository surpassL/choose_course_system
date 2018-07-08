import os
BASE_PAHT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_PAHT,'db')
CLASSES_DB = os.path.join(DB_PATH,'classes')
COURSE_DB = os.path.join(DB_PATH,'course')
SCHOOL_DB = os.path.join(DB_PATH,'school')
STUDENT_DB = os.path.join(DB_PATH,'student')
TEACHER_DB = os.path.join(DB_PATH,'teacher')
LOG_PATH = os.path.join(BASE_PAHT,'log')


#logging配置
# 定义三种日志输出格式 开始

standard_format = '%(asctime)s %(threadName)s:%(thread)d task_id:%(name)s %(filename)s:%(lineno)d ' \
                  '%(levelname)s %(message)s '  # 其中name为get_logger指定的名字

simple_format = '%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s'

id_simple_format = '%(asctime)s  %(message)s'

# 定义日志输出格式 结束

logfile_dir = LOG_PATH  # log文件的目录

logfile_name = 'log.log'  # log文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {  # ''空可以匹配任意名字的logger名，默认配置
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}
# def my_log(name):
#     logging.config.dictConfig(setting.LOGGING_DIC)  # 导入上面定义的logging配置
#     logger = logging.getLogger(name)  # 生成一个log实例
#     return logger