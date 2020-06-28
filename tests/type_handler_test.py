from py_mybatis.type_handler import PyMybatisTypeHandler


def c1(value):
    print("sql_to_python", value)
    return value


def c2(value):
    print("python_to_sql", value)
    return value


p = PyMybatisTypeHandler()
p.register_type_handler('int', 'int', c1, c2)

print(p.convert('int', 'int', 11, PyMybatisTypeHandler.PYTHON2SQL_TYPE_HANDLER_CONVERT_MODE)
      )
