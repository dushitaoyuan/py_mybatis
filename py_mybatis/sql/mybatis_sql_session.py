from py_mybatis.mapper import PyMapper
import os

from .pdbc_sql_template import *
from py_mybatis.py_mybatis_ex import *


# mapper扫描
class MybatisMapperScanner(object):
    def mapper_xml_scan(self, mapper_xml_dir: str):
        mybatis_mapper_dict = MybatisMapperDict()
        for mapper_xml_path in self.__list_mapper(mapper_xml_dir, 'xml'):
            mybatis_mapper_dict.register_mapper(PyMapper(xml_path=mapper_xml_path))
        return mybatis_mapper_dict

    def __list_mapper(self, mapper_xml_dir: str, ext: str):
        all_file = []
        ext = ext.lower()
        file_list = os.listdir(mapper_xml_dir)
        for file in file_list:
            abs_path = os.path.join(mapper_xml_dir, file)
            if os.path.isfile(abs_path) and abs_path.lower().endswith(ext):
                all_file.append(abs_path)
            elif os.path.isdir(abs_path):
                all_file.extend(self.__list_mapper(abs_path, ext))
        return all_file


# mapper 容器
class MybatisMapperDict(object):
    def __init__(self, ):
        self.mapper_dict = {}

    def register_mapper(self, mapper: PyMapper):
        self.mapper_dict[mapper.namespace] = mapper

    """
    proxy statement 
    this sql_id cloud with namespace
    """

    def statement(self, sql_id: str, namespace: str = None, **kwargs):
        if not namespace:
            maybe_sql_id_with_namespace = sql_id.split(',')
            if len(maybe_sql_id_with_namespace) == 2:
                namespace = maybe_sql_id_with_namespace[0]
                sql_id = maybe_sql_id_with_namespace[1]
            else:
                namespace = 'default'
        return self.mapper_dict.get(namespace).statement(sql_id, **kwargs)


# 执行入口
"""
all sql param must be a dict named params
example:
sql_session.select_one(sql_id='test.query',params={'a':1})
"""


class MybatisSqlSession(object):
    def __init__(self, mapper_dict: MybatisMapperDict, dataSource: PooledDB = None,
                 sql_template: PdbcSqlTemplate = None):
        self.mapper_dict = mapper_dict
        if sql_template:
            self.sql_template = sql_template
        elif dataSource:
            self.sql_template = PdbcSqlTemplate(dataSource)
        raise PyMybatisEx("sql_template can't init")

    def beign_tx(self):
        self.connection = self.sql_template.get_connection()

    def select_one(self, sql_id: str, **kwargs):
        return self.sql_template.select_one(self.mapper_dict.statement(sql_id, **kwargs))

    def select_list(self, sql_id: str, row_bound: RowBound = None, **kwargs):
        return self.sql_template.select_list(self.mapper_dict.statement(sql_id, **kwargs), row_bound)

    def insert(self, sql_id: str, **kwargs):
        return self.sql_template.insert(self.mapper_dict.statement(sql_id, **kwargs))

    def delete(self, sql_id: str, **kwargs):
        return self.sql_template.delete(self.mapper_dict.statement(sql_id, **kwargs))

    def update(self, sql_id: str, **kwargs):
        return self.sql_template.update(self.mapper_dict.statement(sql_id, **kwargs))

    def select_page(self, sql_id: str, row_bound: RowBound, count_sql: str = None, **kwargs):
        return self.sql_template.select_page(sql=self.mapper_dict.statement(sql_id, **kwargs), row_bound=row_bound,
                                             count_sql=count_sql)

    def execute_in_connection(self, fun, con=None):
        with self.sql_template.get_connection(con):
            return fun(con)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
