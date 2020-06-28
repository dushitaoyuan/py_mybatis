import contextlib
from DBUtils.PooledDB import PooledDB


class Page(object):
    pageSize: int = None
    pageNum: int = None
    total: int = None
    list: list = None


class RowBound(object):
    def __init__(self, pageNum: int, pageSize: int):
        self.pageSize = pageSize
        self.pageNum = pageNum


"""
基本操作:增删改查,分页
"""


class SqlTemplate(object):
    def __init__(self, dataSource: PooledDB):
        self.dataSource = dataSource

    def insert(self, sql, *args):
        with self._get_connection() as con:
            data = con.cursor().execute(sql, *args)
            con.commit()
            return data

    def update(self, sql, *args):
        with self._get_connection() as con:
            data = con.cursor().execute(sql, *args)
            con.commit()
            return data

    def execute_in_connection(self, fun):
        with self._get_connection() as con:
            return fun(con)

    def delete(self, sql, *args):
        return self.update(sql, *args)

    def select_one(self, sql, *args):
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, *args)
            return cursor.fetchone()

    def select_list(self, sql, *args):
        with self._get_connection() as con:
            cursor = con.cursor()
            cursor.execute(sql, *args)
            return cursor.fetchall()

    def select_page(self, sql, *args, count_sql: str = None, row_bound: RowBound):
        with self._get_connection() as con:
            cursor = con.cursor()
            page_result = Page()
            page_result.pageNum = row_bound.pageNum
            page_result.pageSize = row_bound.pageSize
            if count_sql is None:
                cursor.execute(count_query(sql), *args)
                page_result.total = cursor.fetchone()['count(*)']
            else:
                cursor.execute(count_sql, *args)
                page_result.total = get_one_value(cursor.fetchone())
            cursor.execute(limit_query(sql, row_bound), *args)
            page_result.list = cursor.fetchall()
            return page_result

    @contextlib.contextmanager
    def _get_connection(self):
        connection = self.dataSource.connection()
        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()


"""
分页查询
"""


def count_query(sql: str):
    return "select count(*) from (" + sql + ") temp"


def limit_query(sql: str, row_bound: RowBound):
    start = (row_bound.pageNum - 1) * row_bound.pageSize
    return sql + "limit {},{}".format(start, row_bound.pageSize)


def get_one_value(count_dict: dict):
    for count in count_dict.values():
        return count
