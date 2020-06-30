from py_mybatis.sql.mybatis_sql_session import MybatisMapperScanner, MybatisSqlSession, PooledDB
import pymysql
import os

import unittest

import time


class PyMybatisTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.abspath("./")
        mapper_scanner = MybatisMapperScanner()
        mybatis_mapper_dict = mapper_scanner.mapper_xml_scan(mapper_xml_dir=path)
        pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            maxcached=5,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host="localhost",
            user="root",
            password="root",
            database="api_user",
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8'
        )
        cls.sql_session = MybatisSqlSession(mapper_dict=mybatis_mapper_dict, dataSource=pool)
        cls.sql_namespace = 'Test.'

    def test_base(self):
        self.sql_id = self.sql_namespace + 'testBasic'
        print("============{}============,sql_result:{}".format(self.sql_id, self.sql_session.select_list(self.sql_id)))

    def test_parameters(self):
        self.sql_id = self.sql_namespace + 'testParameters'
        params = {'category': 'apple', 'price': '15.0', 'type': '001', 'content': '图书'}

        print("============{}============,sql_result:{}".format(self.sql_id, self.sql_session.select_list(self.sql_id,
                                                                                                          params=params)))

    def test_include(self):
        self.sql_id = 'testInclude'
        params = {'category': 'apple'}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_list(self.sql_id,
                                                                                             params=params)))

    def test_if(self):
        self.sql_id = 'testIf'
        params = {'category': 'apple', 'price': 5}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_one(self.sql_id,
                                                                                            params=params)))

    def test_trim(self):
        self.sql_id = 'testTrim'
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_one(self.sql_id)))

    def test_where(self):
        self.sql_id = 'testWhere'
        params = {'category': 'apple', 'price': 500}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_one(self.sql_id,
                                                                                            params=params)))

    def test_set(self):
        self.sql_id = 'testSet'
        params = {'category': 'apple', 'price': 500, 'name': 'name1'}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.update(self.sql_id,
                                                                                        params=params)))

    def test_choose(self):
        self.sql_id = 'testChoose'
        params = {'age': 1, 'sex': '1', 'name': 'name', 'price': 'price', 'category': 'banana'}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_list(self.sql_id,
                                                                                             params=params)))

    def test_foreach(self):
        self.sql_id = 'testForeach'
        params = {'names': ['name1', 'name2', 'name3']}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_list(self.sql_id,
                                                                                             params=params)))

    def test_bind(self):
        self.sql_id = 'testBind'
        params = {'name': 'name'}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_list(self.sql_id,
                                                                                             params=params)))

    def test_choose_native(self):
        self.sql_id = 'testChooseNative'
        params = {'category': 'banana', 'price': 500, 'name': 'name1'}
        self.sql_id = self.sql_namespace + self.sql_id
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.select_list(self.sql_id,
                                                                                             params=params)))

    def test_insert_multi(self):
        self.sql_id = 'testInsertMulti'
        self.sql_id = self.sql_namespace + self.sql_id

        create_time = time.localtime()
        params = {'fruits': [

            {
                'id': 1,
                'name': 'apple',
                'category': 'apple',
                'price': 5.0,
                'create_time': create_time
            },
            {
                'id': 2,

                'name': 'banana',
                'category': 'banana',
                'price': 3.0,
                'create_time': create_time
            },
            {
                'id': 3,
                'name': 'pear',
                'category': 'pear',
                'price': 4.0,
                'create_time': create_time
            },
        ]}
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.insert(self.sql_id,
                                                                                        params=params)))

    def test_insert_selective(self):
        self.sql_id = 'testInsertSelective'
        self.sql_id = self.sql_namespace + self.sql_id
        params = {
            'id': 20,
            'name': 'apple',
            'category': 'apple',
            'price': 5.0
        }
        print("============{}============,sql_result:{}".format(self.sql_id,
                                                                self.sql_session.insert(self.sql_id,
                                                                                        params=params)))

    """

    self.sql_session.begin_tx():
    会在当前线程的thread_local下绑定一个connection 此后执行所有方法都会在一个 connection下
    除非手动调用 self.sql_session.close(): 关闭连接
    self.sql_session.commit():提交事务
    self.sql_session.rollback(): 关闭事务
    
    未调用:self.sql_session.begin_tx()方法:每次调用sql_session 都会新建一个连接,建议使用连接池
    参考用法:
            try:
            self.sql_session.begin_tx()
            .... do_something_tx
            self.sql_session.commit()
            print("commit")
        except Exception as e:
            print("exception rollback", e)
            self.sql_session.rollback()
        finally:
            print("finally close")
            self.sql_session.close()
    
    """

    def test_tx(self):
        print("============{}============".format('test_tx'))
        """
        template method
        """
        fruits = [

            {
                'id': 4,
                'name': 'apple',
                'category': 'apple',
                'price': 5.0
            },
            {
                'id': 5,

                'name': 'banana',
                'category': 'banana',
                'price': 3.0
            },
            {
                'id': 6,
                'name': 'pear',
                'category': 'pear',
                'price': 4.0
            },
        ]
        try:
            self.sql_session.begin_tx()
            for index, item in enumerate(fruits):
                self.sql_session.insert(sql_id='Test.insertOne', params=item)
                if index > 1:
                    raise Exception('rollback test')
            self.sql_session.commit()
            print("commit")
        except Exception as e:
            print("exception rollback", e)
            self.sql_session.rollback()
        finally:
            print("finally close")
            self.sql_session.close()


if __name__ == '__main__':
    unittest.main()
