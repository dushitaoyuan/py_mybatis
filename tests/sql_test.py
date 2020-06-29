from py_mybatis.sql.pdbc_sql_template import *
from py_mybatis.mapper import PyMapper
import pymysql
import time

mysql_pool = PooledDB(
    creator=pymysql,
    maxconnections=6,
    mincached=2,
    maxcached=5,
    blocking=True,
    maxusage=None,
    setsession=[],
    ping=0,
    host="192.168.3.1",
    user="root",
    password="root",
    database="api_user",
    cursorclass=pymysql.cursors.DictCursor,
    charset='utf8'
)
sql_template = PdbcSqlTemplate(dataSource=mysql_pool)



py_mapper = PyMapper(xml_path='test.xml')

print(sql_template.select_list(py_mapper.statement('testBasic')))

params = {'name': 'apple', 'create_time': time.localtime()}
print(sql_template.select_list(py_mapper.statement('test_function', params=params)))

params = {'category': 'apple', 'price': 5, 'type': 0}
print(sql_template.select_list(py_mapper.statement('testParameters', params=params)))

params = {'category': 'apple', 'price': 500, 'type': 0}
print(sql_template.select_list(py_mapper.statement('testInclude', params=params)))

params = {'category': 'pear', 'price': 5}
print(sql_template.select_list(py_mapper.statement('testIf', params=params)))

params = {'category': 'pear', 'price': 5}
print(sql_template.select_list(py_mapper.statement('testTrim', params=params)))

params = {'category': 'pear', 'price': 5}
print(sql_template.select_list(py_mapper.statement('testWhere', params=params)))

params = {'category': 'pear', 'name': 'apple', 'price': 5}
print(sql_template.select_list(py_mapper.statement('testSet', params=params)))

params = {'names': ['香蕉', '梨', '苹果']}
print(sql_template.select_list(py_mapper.statement('testForeach', params=params)))

params = {'names': ['香蕉', '梨', '苹果']}

now = time.localtime()
# params = {'fruits': [
#     {
#         'id': 4,
#         'name': 'apple',
#         'category': 'apple',
#         'price': 5.0,
#         'create_time': now
#     },
#     {
#         'id': 5,
#         'name': 'banana',
#         'category': 'banana',
#         'price': 3.0,
#         'create_time': now
#     },
#     {
#         'id': 6,
#         'name': 'pear',
#         'category': 'pear',
#         'price': 4.0,
#         'create_time': now
#     },
# ]}
#
# print(sql_template.insert(py_mapper.statement('testInsertMulti', params=params)))

# params = {'id': 4}
# print(sql_template.delete(py_mapper.statement('deleteById', params=params)))
