from py_mybatis import PyMapper, PY_MYBATIS_TYPE_HANDLER, PyMybatisTypeHandler

mapper = PyMapper(xml_path='test.xml')
import time

# for statement_id in mapper.list_statement():
#     print(statement_id)

# params = {'name': 'name', 'time': time.localtime()}
# print(mapper.statement('test_function', params=params))


sql_id = 'testInsertMulti'
params = {'fruits': [
    {'name': 'apple',
     'category': 'apple',
     'price': 5.0
     },
    {'name': 'banana',
     'category': 'banana',
     'price': 3.0
     },
    {'name': 'pear',
     'category': 'pear',
     'price': 4.0
     },
]}

print("============{}============".format(sql_id))
statement = mapper.statement(sql_id=sql_id,
                                       reindent=True,  params=params)
print(statement)