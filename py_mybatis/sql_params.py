# -*- coding: UTF-8 -*-
import re

type_mapping = {
    'NUM': ['TINYINT', 'SMALLINT', 'INTEGER', 'BIGINT', 'BIT', 'DECIMAL', 'DOUBLE', 'FLOAT', 'NUMERIC'],
    'BOOLEAN': ['BOOLEAN'],
    'DATE': ['DATE', 'TIME', 'TIMESTAMP'],
    'STRING': ['CHAR', 'VARCHAR', 'NCHAR', 'NVARCHAR', 'LONGNVARCHAR', 'LONGVARCHAR'],
    'BINARY': ['BINARY', 'VARBINARY', 'LONGVARBINARY', 'BLOB'],
    'OTHER': ['ARRAY', 'CLOB', 'CURSOR', 'DATALINK', 'DATETIMEOFFSET', 'DISTINCT', 'NCLOB',
              'NULL', 'OTHER', 'REAL', 'REF', 'ROWID', 'SQLXML', 'STRUCT', 'UNDEFINED']

}
# function regex:example $f{func_example(value)}
param_function_regex = re.compile('.+?\(.+?\)')


class SqlParamRegex(object):
    def __init__(self, regex: str, prefix: str):
        self.regex = re.compile(regex)
        self.prefix = prefix

    def resolve_param(self, param: str):
        param = param.replace(self.prefix + '{', '').replace('}', '')
        if param_function_regex.match(param):
            function_name = param[0:param.find('(')]
            return SqlParam(function_expression=param, is_function=True, function_name=function_name)
        else:
            return SqlParam(param_name=param.split(',')[0])


class SqlParam(object):
    def __init__(self, param_name: str = None, function_expression: str = None, is_function: bool = False,
                 function_name: str = None):
        self.is_function = is_function
        self.param_name = param_name
        self.function_expression = function_expression
        self.function_name = function_name

    def __str__(self):
        return 'is_function:%s ,param_name:%s,function_expression:%s,function_name:%s' % (
            self.is_function, self.param_name, self.function_expression, self.function_name)


class PyMybatisParam(object):
    def __init__(self, sql_param: SqlParam,
                 full_name: str = None, sql_type: str = None,
                 python_type: str = None,
                 type_handler: str = None
                 ):
        self.sql_param = sql_param
        self.full_name = full_name
        self.sql_type = sql_type
        self.python_type = python_type
        self.type_handler = type_handler
        self.param_name = sql_param.param_name

    def __str__(self):
        return 'sql_param:%s ,full_name:%s,sql_type:%s,python_type:%s,type_handler:%s,param_name:%s' % (
            self.sql_param, self.full_name, self.sql_type, self.python_type, self.type_handler, self.param_name
        )


sql_regex_list = [SqlParamRegex('\#\{.+?\}', '#'), SqlParamRegex('\$\{.+?\}', '$'),
                  SqlParamRegex('\$f\{.+?\}', '$f'), ]


def get_params(child):
    """
    Get SQL Params
    example: #{age,pythonType=int,sqlType=NUMERIC,typeHandler=MyTypeHandler}
    change: '#','$'
    :return:
    """
    p = re.compile('\S')
    # Remove empty info
    child_text = child.text if child.text else ''
    child_tail = child.tail if child.tail else ''
    child_text = child_text if p.search(child_text) else ''
    child_tail = child_tail if p.search(child_tail) else ''
    convert_string = child_text + child_tail
    param_list = []
    for sql_regex in sql_regex_list:
        tmp_params = []
        match = sql_regex.regex.findall(convert_string)
        # tmp_unique_params
        tmp_params += sorted(set(match), key=match.index)
        """
        get sql_type、python_type,type_handler
        """
        for param in tmp_params:
            sql_param = sql_regex.resolve_param(param)
            mybatis_param = PyMybatisParam(full_name=param, sql_param=sql_param)
            if not sql_param.is_function:
                mybatis_param.name = sql_param.param_name
                mybatis_param.sql_type = __get_regex_value('(\s*sql_type\s*=\s*)(?P<sql_type>\w+)?', param, 'sql_type')
                mybatis_param.python_type = __get_regex_value('(\s*python_type\s*=\s*)(?P<python_type>\w+)?', param,
                                                              'python_type')
                mybatis_param.type_handler = __get_regex_value('(\s*type_handler\s*=\s*)(?P<type_handler>\w+)?', param,
                                                               'type_handler')
            param_list.append(mybatis_param)

    return param_list


def __get_regex_value(regex: str, param: str, group: str):
    m = re.search(regex, param)
    return m.group(group).strip() if m else None


def get_sql_param(param_text):
    """
    Get SQL Params
    example: #{param_name}
    prefix: '#','$','$f'
    :return:
    """
    param_list = []
    for sql_param_regex in sql_regex_list:
        tmp_params = []
        match = sql_param_regex.regex.findall(param_text)
        # tmp_unique_params
        tmp_params += sorted(set(match), key=match.index)
        for param in tmp_params:
            sql_param = sql_param_regex.resolve_param(param)
            mybatis_param = PyMybatisParam(full_name=param, sql_param=sql_param)
            if not sql_param.is_function:
                mybatis_param.name = sql_param.param_name
                mybatis_param.sql_type = __get_regex_value('(\s*sql_type\s*=\s*)(?P<sql_type>\w+)?', param, 'sql_type')
                mybatis_param.python_type = __get_regex_value('(\s*python_type\s*=\s*)(?P<python_type>\w+)?', param,
                                                              'python_type')
                mybatis_param.type_handler = __get_regex_value('(\s*type_handler\s*=\s*)(?P<type_handler>\w+)?', param,
                                                               'type_handler')
            param_list.append(mybatis_param)
    return param_list


# def say_sql_param(param_text: str):
#     for p in get_sql_param(param_text):
#         print(p)
#
#
# say_sql_param('#{age,pythonType=int,sqlType=NUMERIC,typeHandler=MyTypeHandler}')
#
# say_sql_param('$f{fun1(name)}')
#
# say_sql_param('$f{fun1(name1,name2)}')

