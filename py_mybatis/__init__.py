# -*- coding: UTF-8 -*-
"""
PyMybatis
----------------------
Generate SQL Statements from the MyBatis3 Mapper XML file
usage:
   >>> import mybatis_mapper2sql
   >>> mapper, xml_raw_text = mybatis_mapper2sql.create_mapper(xml='mybatis_mapper.xml')
   >>> statement = mybatis_mapper2sql.get_statement(mapper)
   >>> print(statement)
"""
from .mapper import PyMapper
from .type_handler import PY_MYBATIS_TYPE_HANDLER, PyMybatisTypeHandler
from .py_mybatis_ex import PyMybatisEx

from .mapper_func import PyFunction, PY_PARAM_FUNCTION, PY_RESULT_FUNCTION

from .sql_params import get_params, get_sql_param
