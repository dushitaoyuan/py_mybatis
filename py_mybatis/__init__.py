# -*- coding: UTF-8 -*-
"""
PyMybatis
----------------------
Generate SQL Statements from the MyBatis3 Mapper XML file
usage:
   >>> import py_mybatis
   >>> sql_template = PdbcSqlTemplate(dataSource=mysql_pool)
   >>> py_mapper = PyMapper(xml_path='test.xml')
   >>> params = {'name': 'apple', 'create_time': time.localtime()}
   >>> print(sql_template.select_list(py_mapper.statement('test_function', params=params)))

   or use sql_template only
   sql_template = PdbcSqlTemplate(dataSource=mysql_pool)

"""
from .mapper import PyMapper
from .sql import PooledDB, PdbcSqlTemplate, MybatisMapperDict, MybatisMapperScanner, MybatisSqlSession, Page, RowBound

from .type_handler import PY_MYBATIS_TYPE_HANDLER, PyMybatisTypeHandler

from .mapper_func import PyFunction, PY_PARAM_FUNCTION, PY_RESULT_FUNCTION

