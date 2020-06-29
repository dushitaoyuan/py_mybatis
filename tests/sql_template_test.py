from py_mybatis.sql.pdbc_sql_template import *
import pymysql

import unittest


def query_function(connection):
    cursor = connection.cursor()
    try:
        cursor.execute('select * from fruits')
        data = cursor.fetchall()
        connection.commit()
        return data
    finally:
        cursor.close()


class PyMybatisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql_template = PdbcSqlTemplate(dataSource=PooledDB(
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
        ))

    def test_select_list(self):
        print("============{}============".format('select_with row_bound'))
        print(
            self.sql_template.select_list(sql="select * from fruits where id in (%s,%s,%s)",
                                          row_bound=RowBound(1, 2), args=(1, 2, 3))
        )
        print("============{}============".format('select_only'))
        print(
            self.sql_template.select_list(sql="select * from fruits where id in (%s,%s,%s)", args=(1, 2, 3))
        )

    def test_select_one(self):
        print("============{}============".format('test_select_one'))
        print(
            self.sql_template.select_one(sql="select * from fruits where id=%s", args=(1))
        )

    def test_select_with_no_params(self):
        print("============{}============".format('test_select_with_no_params'))
        print(
            self.sql_template.select_one(sql="select * from fruits where id=1")
        )

    def test_select_page(self):
        print("============{}============".format('test_select_page'))
        print(
            self.sql_template.select_page(sql="select * from fruits", row_bound=RowBound(1, 2))
        )

    def test_delete(self):
        print("============{}============".format('test_delete'))
        row = self.sql_template.delete(
            sql="delete from fruits where id in(%s,%s,%s)",
            args=(10, 11, 9))
        print(row)

    def test_insert_one(self):
        print("============{}============".format('test_insert_one'))
        row = self.sql_template.insert(sql="insert into fruits(id,name,price,category) values(%s,%s,%s,%s)",
                                       args=(10, '菠萝', 10, 'boluo'))
        print(row)

    def test_insert_mul(self):
        print("============{}============".format('test_insert_mul'))
        row = self.sql_template.insert_batch(
            sql="insert into fruits(id,name,price,category) values(%s,%s,%s,%s)",
            args=((11, '菠萝', 11, 'boluo11'), (9, '菠萝1', 9, 'boluo9')))
        print(row)

    def test_query_in_connection(self):
        print("============{}============".format('test_query_in_connection'))
        print(self.sql_template.execute_in_connection(query_function))


if __name__ == '__main__':
    unittest.main()
