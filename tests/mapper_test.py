from py_mybatis import PyMapper, PY_MYBATIS_TYPE_HANDLER, PyMybatisTypeHandler

mapper = PyMapper(xml_path='test.xml')
import time

for statement_id in mapper.list_statement():
    print(statement_id)

params = {'name': 'name', 'create_time': time.localtime()}
print(mapper.statement('test_function', params=params))

now = time.localtime()
sql_id = 'testInsertMulti'
params = {'fruits': [
    {
        'id': 1,
        'name': 'apple',
        'category': 'apple',
        'price': 5.0,
        'create_time': now
    },
    {
        'id': 2,
        'name': 'banana',
        'category': 'banana',
        'price': 3.0,
        'create_time': now

    },
    {
        'id': 3,
        'name': 'pear',
        'category': 'pear',
        'price': 4.0,
        'create_time': now
    },
]}

print("============{}============".format(sql_id))
statement = mapper.statement(sql_id=sql_id,
                             reindent=True, params=params)
print(statement)
