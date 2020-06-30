import sqlparse
import xml.etree.ElementTree as ET
from .sql_params import get_params, PyMybatisParam
from .sql_util import replace_cdata, convert_cdata, param_str
from .type_handler import PyMybatisTypeHandler, PY_MYBATIS_TYPE_HANDLER
from .mapper_func import PY_PARAM_FUNCTION

from .string_util import *

sql_id_type_list = ['sql', 'select', 'insert', 'update', 'delete']


class PyMapper(object):
    def __init__(self, xml_path: str = None, xml_text: str = None):
        if xml_text is None:
            with open(xml_path, "r", encoding='UTF-8') as f:
                xml_text = f.read()
        self.mapper = {}
        self.xml_text = xml_text
        raw_text = replace_cdata(xml_text)
        mapper_xml_tree = ET.fromstring(raw_text)
        self.namespace = mapper_xml_tree.attrib.get("namespace", 'default')
        for sub_statement_node in mapper_xml_tree:
            if sub_statement_node.tag in sql_id_type_list:
                sql_id = sub_statement_node.attrib.get('id')
                self.mapper[sql_id] = sub_statement_node

    def list_statement(self):
        return self.mapper.keys()

    def statement(self, sql_id: str, **kwargs):
        """
        Get SQL Statement By sql_id
        Formatting of SQL Statements
        :return:
        """
        # format kwargs
        kwargs = kwargs if kwargs else {'reindent': True, 'strip_comments': True}
        # get sql
        statement = ''
        child = self.mapper.get(sql_id)
        statement += convert_children(self.mapper, child, **kwargs)
        # The child element has children
        for next_child in child:
            statement += convert_children(self.mapper, next_child, **kwargs)
        return sqlparse.format(statement, **kwargs)


def convert_children(mybatis_mapper, child, **kwargs):
    """
    Get children info
    :param mybatis_mapper:
    :param child:
    :param kwargs: native: parse follow the native rules
    :return:
    """
    if child.tag in sql_id_type_list:
        return convert_parameters(child, text=True, tail=True, **kwargs)
    elif child.tag == 'include':
        return convert_include(mybatis_mapper, child, **kwargs)
    elif child.tag == 'if':
        return convert_if(mybatis_mapper, child, **kwargs)
    elif child.tag in ('choose', 'when', 'otherwise'):
        return convert_choose_when_otherwise(mybatis_mapper, child, **kwargs)
    elif child.tag in ('trim', 'where', 'set'):
        return convert_trim_where_set(mybatis_mapper, child, **kwargs)
    elif child.tag == 'foreach':
        return convert_foreach(mybatis_mapper, child, **kwargs)
    elif child.tag == 'bind':
        return convert_bind(child, **kwargs)
    else:
        return ''


def convert_parameters(child, text=False, tail=False, **kwargs):
    """
    Get child text or tail
    :param child:
    :param text:
    :param tail:
    :return:
    """
    p = re.compile(r'\S')
    # Remove empty info
    child_text = child.text if child.text else ''
    child_tail = child.tail if child.tail else ''
    child_text = child_text if p.search(child_text) else ''
    child_tail = child_tail if p.search(child_tail) else ''
    # all
    if text and tail:
        convert_string = child_text + child_tail
    # only_text
    elif text:
        convert_string = child_text
    # only_tail
    elif tail:
        convert_string = child_tail
    else:
        convert_string = ''
    # replace params
    mybatis_param_list = get_params(child)
    for mybatis_param in mybatis_param_list:
        convert_value = ''
        if mybatis_param.sql_param.is_function:
            # eval function
            convert_value = __eval_function(mybatis_param, **kwargs)
        else:
            # 类型转换
            param_value = __get_param(mybatis_param.param_name, **kwargs)
            convert_value = PY_MYBATIS_TYPE_HANDLER.convert(mybatis_param.python_type, mybatis_param.sql_type,
                                                            param_value,
                                                            PyMybatisTypeHandler.PYTHON2SQL_TYPE_HANDLER_CONVERT_MODE)
        convert_string = convert_string.replace(mybatis_param.full_name, convert_value, 1)
    # convert CDATA string
    convert_cdata(convert_string)
    return convert_string


def convert_include(mybatis_mapper, child, **kwargs):
    # Add Properties
    properties = kwargs.get('properties') if kwargs.get('properties') else dict()
    for next_child in child:
        if next_child.tag == 'property':
            properties[next_child.attrib.get('name')] = next_child.attrib.get('value')
    convert_string = ''
    include_child_id = child.attrib.get('refid')
    for change in ['#', '$']:
        string_regex = '\\' + change + '\{.+?\}'
        if re.match(string_regex, include_child_id):
            include_child_id = include_child_id.replace(change + '{', '').replace('}', '')
            include_child_id = properties.get(include_child_id)
            break
    include_child = mybatis_mapper.get(include_child_id)
    convert_string += convert_children(mybatis_mapper, include_child, **kwargs)
    # add include text
    convert_string += convert_parameters(child, text=True, **kwargs)
    for next_child in include_child:
        kwargs['properties'] = properties
        convert_string += convert_children(mybatis_mapper, next_child, **kwargs)
    # add include tail
    convert_string += convert_parameters(child, tail=True, **kwargs)
    return convert_string


def convert_if(mybatis_mapper, child, **kwargs):
    convert_string = ''
    test = child.attrib.get('test')
    if not __calc_condition(test, **kwargs):
        return convert_string
    # Add if text
    convert_string += convert_parameters(child, text=True, **kwargs)
    for next_child in child:
        convert_string += convert_children(mybatis_mapper, next_child, **kwargs)
        convert_string = __add_sql_strip_comments(convert_string, '-- if(' + test + ')\n', **kwargs)
    # Add if tail
    convert_string += convert_parameters(child, tail=True, **kwargs)
    return convert_string


def convert_choose_when_otherwise(mybatis_mapper, child, **kwargs):
    # native
    native = kwargs.get('native')
    when_element_cnt = kwargs.get('when_element_cnt', 0)
    convert_string = ''
    when_test_result = False
    for next_child in child:
        if next_child.tag == 'when':
            if native and when_element_cnt >= 1:
                break
            else:
                test = next_child.attrib.get('test')
                if __calc_condition(test, **kwargs):
                    when_test_result = True
                if when_test_result:
                    convert_string += convert_parameters(next_child, text=True, tail=True, **kwargs)
                    convert_string = __add_sql_strip_comments(convert_string, '-- if(' + test + ')', **kwargs)
                    convert_string += convert_children(mybatis_mapper, next_child, **kwargs)
                    for sub_child in next_child:
                        convert_string += convert_children(mybatis_mapper, sub_child, **kwargs)
                when_element_cnt += 1
                kwargs['when_element_cnt'] = when_element_cnt
        elif next_child.tag == 'otherwise' and not when_test_result:
            convert_string += convert_parameters(next_child, text=True, tail=True)
            convert_string = __add_sql_strip_comments(convert_string, '-- otherwise', **kwargs)
            convert_string += convert_children(mybatis_mapper, next_child, **kwargs)
            for sub_child in next_child:
                convert_string += convert_children(mybatis_mapper, sub_child, **kwargs)

    return convert_string


def convert_trim_where_set(mybatis_mapper, child, **kwargs):
    if child.tag == 'trim':
        prefix = child.attrib.get('prefix')
        suffix = child.attrib.get('suffix')
        prefix_overrides = child.attrib.get('prefixOverrides')
        suffix_overrides = child.attrib.get('suffixOverrides')
    elif child.tag == 'set':
        prefix = 'SET'
        suffix = None
        prefix_overrides = None
        suffix_overrides = ','
    elif child.tag == 'where':
        prefix = 'WHERE'
        suffix = None
        prefix_overrides = 'and|or'
        suffix_overrides = None
    else:
        return ''

    convert_string = ''
    # Add trim/where/set text
    convert_string += convert_parameters(child, text=True, **kwargs)
    # Convert children first
    for next_child in child:
        convert_string += convert_children(mybatis_mapper, next_child, **kwargs)
    # Remove prefixOverrides
    if prefix_overrides:
        convert_string = ' ' + replace_sql_first(convert_string, prefix_overrides, '')
    # Remove suffixOverrides
    if suffix_overrides:
        convert_string = ' ' + replace_sql_last(convert_string, suffix_overrides, '')
    # Add Prefix if String is not empty
    if re.search(r'\S', convert_string):
        if prefix:
            convert_string = ' ' + prefix + ' ' + convert_string
        if suffix:
            convert_string = convert_string + ' ' + suffix
    # Add trim/where/set tail
    convert_string += convert_parameters(child, tail=True, **kwargs)
    return convert_string


def convert_foreach(mybatis_mapper, child, **kwargs):
    collection = child.attrib.get('collection')
    collection_value = __get_param(collection, **kwargs)
    if not collection_value:
        return ''
    item = child.attrib.get('item')
    index = child.attrib.get('index')
    open = child.attrib.get('open', '')
    close = child.attrib.get('close', '')
    separator = child.attrib.get('separator', '')
    convert_string = ''
    # for each items
    convert_string += open
    last = len(collection_value) - 1
    mybatis_param_list = get_params(child)
    for_each_text = child.text
    for index, item_value in enumerate(collection_value):
        convert_string += __calc_foreach_value(for_each_text, mybatis_param_list, item, item_value)
        if index != last:
            convert_string += separator
    convert_string += close
    return convert_string


def convert_bind(child, **kwargs):
    """
    :param child:
    :return:
    """
    name = child.attrib.get('name')
    value = child.attrib.get('value')
    convert_string = ''
    params = __add_param(name, value, **kwargs)
    params[name] = __calc_condition(value, params=params)
    convert_string += convert_parameters(child, tail=True, **kwargs)
    convert_string = convert_string.replace(name, value)
    return convert_string


# 添加sql注释
def __add_sql_strip_comments(sql: str, sql_comment: str, **kwargs):
    strip_comments = True if 'strip_comments' in kwargs and kwargs['strip_comments'] else False
    if strip_comments:
        return sql + sql_comment
    else:
        return sql


# 计算标签条件
def __calc_condition(condition: str, **kwargs):
    params = kwargs['params'] if 'params' in kwargs else {}
    return eval(condition, locals())


# 计算foreach 标签值
def __calc_foreach_value(for_each_text: str, mybatis_param_list, item, item_value):
    for param in mybatis_param_list:
        sql_param = param.sql_param
        if not sql_param.is_function:
            value_expression = sql_param.param_name.replace(item, 'item_value', 1)
            calc_value = eval(value_expression, locals())
            for_each_text = for_each_text.replace(param.full_name, param_str(calc_value), 1)
        else:
            function_expression = sql_param.function_expression
            # 查找函数
            fun = PY_PARAM_FUNCTION.get_func(sql_param.function_name)
            # 替换表达式
            function_expression = sql_param.function_expression.replace(sql_param.function_name, 'fun', 1)
            function_expression = function_expression.replace(item, 'item_value', 1)
            # 执行函数
            calc_value = eval(function_expression, locals())
            for_each_text = for_each_text.replace(param.full_name, param_str(calc_value), 1)
    return for_each_text


# 函数计算
def __eval_function(mybatis_param: PyMybatisParam, **kwargs):
    params = kwargs['params'] if 'params' in kwargs else {}
    sql_param = mybatis_param.sql_param
    fun = PY_PARAM_FUNCTION.get_func(sql_param.function_name)
    function_expression = sql_param.function_expression.replace(sql_param.function_name, 'fun', 1)
    return eval(function_expression, locals())


# 获取参数
def __get_param(param_key: str, **kwargs):
    params = kwargs['params'] if 'params' in kwargs else {}
    if param_key in params:
        return params[param_key]
    return None


# 添加参数
def __add_param(param_key: str, param_value, **kwargs):
    params = kwargs['params'] if 'params' in kwargs else {}
    params[param_key] = param_value
    return params
