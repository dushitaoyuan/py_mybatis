"""
functions

"""
import time

from .sql_util import *


def like(value):
    return sql_string_format(value)


def time_format(date_value, format: str = '%Y-%m-%d %H:%M:%S'):
    return sql_string_format(time.strftime(format, date_value))


default_fun_dict = {}
default_fun_dict['like'] = like

default_fun_dict['time_format'] = time_format
