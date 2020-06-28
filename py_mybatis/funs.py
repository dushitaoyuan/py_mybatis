"""
functions

"""
import time


def like(value):
    return '%' + value + '%'


def time_format(date_value, format: str = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(format, date_value)


fun_dict = {}
fun_dict['like'] = like

fun_dict['time_format'] = time_format
