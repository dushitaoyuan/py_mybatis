from .sql_util import *


class TypeHandlerConvertor(object):
    def __init__(self, python_type_name: str, sql_type_name: str, sql2python_fun, python2sql_fun):
        self.python_type_name = python_type_name
        self.sql_type_name = sql_type_name
        self.sql2python_fun = sql2python_fun
        self.python2sql_fun = python2sql_fun

    def support(self, type_from: str, type_to: str, convert_mode: int):
        if convert_mode == PyMybatisTypeHandler.PYTHON2SQL_TYPE_HANDLER_CONVERT_MODE:
            return self.python_type_name == type_from and self.sql_type_name == type_to
        elif convert_mode == PyMybatisTypeHandler.SQL2PYTHON_TYPE_HANDLER_CONVERT_MODE:
            return self.python_type_name == type_to and self.sql_type_name == type_from
        return False

    def convert(self, convert_mode: int, type_value):
        if convert_mode == PyMybatisTypeHandler.PYTHON2SQL_TYPE_HANDLER_CONVERT_MODE:
            return self.__python_type_to_sql(type_value)
        elif convert_mode == PyMybatisTypeHandler.SQL2PYTHON_TYPE_HANDLER_CONVERT_MODE:
            return self.__sql_type_to_python(type_value)

    # sql type-> python type
    def __sql_type_to_python(self, sql_type_value):
        if self.sql2python_fun:
            return self.sql2python_fun(sql_type_value)
        else:
            return sql_type_value

    # python type-> sql type
    def __python_type_to_sql(self, python_type_value):
        if self.sql2python_fun:
            return self.python2sql_fun(python_type_value)
        else:
            return python_type_value


class PyMybatisTypeHandler(object):
    PYTHON2SQL_TYPE_HANDLER_CONVERT_MODE = 0
    SQL2PYTHON_TYPE_HANDLER_CONVERT_MODE = 1

    def __init__(self):
        self.type_handler_support_list = []

    def register_type_handler(self, python_type_name: str = None, sql_type_name: str = None, sql2python_fun=None,
                              python2sql_fun=None,
                              type_handler_convertor: TypeHandlerConvertor = None):
        if type_handler_convertor:
            self.type_handler_support_list.append(type_handler_convertor)
        else:
            self.type_handler_support_list.append(
                TypeHandlerConvertor(python_type_name, sql_type_name, sql2python_fun, python2sql_fun))

    def convert(self, type_from: str, type_to: str, type_value, convert_mode: int):
        if type_value and type_from and type_to:
            type_handler = self.__find_type_handler(type_from, type_to, convert_mode)
            if type_handler:
                type_value = type_handler.convert(convert_mode, type_value)
        return param_str(type_value)

    def __find_type_handler(self, type_from: str, type_to: str, convert_mode: int):
        for type_handler in self.type_handler_support_list:
            if type_handler.support(type_from, type_to, convert_mode):
                return type_handler


PY_MYBATIS_TYPE_HANDLER = PyMybatisTypeHandler()
