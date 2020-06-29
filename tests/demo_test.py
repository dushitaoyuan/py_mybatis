import os
import unittest
from py_mybatis import PyMapper

import time

base_dir = os.path.abspath(os.path.dirname(__file__))


class PyMybatisTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mapper = PyMapper(xml_path='test.xml')

    def test_base(self):
        self.sql_id = 'testBasic'
        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True)
        print(self.statement)

    def test_parameters(self):
        self.sql_id = 'testParameters'
        params = {'category': 'cat', 'price': '15.0', 'type': '001', 'content': '图书'}

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id,
                                               reindent=True, params=params)
        print(self.statement)

    def test_include(self):
        self.sql_id = 'testInclude'
        params = {'category': 'cat'}

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True,
                                               params=params)
        print(self.statement)

    def test_if(self):
        self.sql_id = 'testIf'
        params = {'category': 'apple', 'price': 500}
        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id,
                                               reindent=True, params=params)
        print(self.statement)

    def test_trim(self):
        self.sql_id = 'testTrim'
        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True)
        print(self.statement)

    def test_where(self):
        self.sql_id = 'testWhere'
        params = {'category': 'apple', 'price': 500}
        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True,
                                               params=params)
        print(self.statement)

    def test_set(self):
        self.sql_id = 'testSet'
        print("============{}============".format(self.sql_id))
        params = {'category': 'apple', 'price': 500, 'name': 'name1'}

        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True,
                                               params=params)
        print(self.statement)

    def test_choose(self):
        self.sql_id = 'testChoose'
        print("============{}============".format(self.sql_id))
        params = {'age': 1, 'sex': '1', 'name': 'name', 'price': 'price', 'category': 'banana'}
        statement = self.mapper.statement(sql_id="testChoose", params=params)
        print(statement)

    def test_foreach(self):
        self.sql_id = 'testForeach'
        params = {'names': ['name1', 'name2', 'name3']}

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True,
                                               params=params)
        print(self.statement)

    def test_bind(self):
        self.sql_id = 'testBind'
        params = {'name': 'name'}

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id, reindent=True,
                                               params=params)
        print(self.statement)

    def test_choose_native(self):
        self.sql_id = 'testChooseNative'
        params = {'category': 'banana', 'price': 500, 'name': 'name1'}

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id,
                                               reindent=True, native=True, params=params)
        print(self.statement)

    def test_insert_multi(self):
        self.sql_id = 'testInsertMulti'
        create_time = time.localtime()
        params = {'fruits': [

            {
                'id': 1,
                'name': 'apple',
                'category': 'apple',
                'price': 5.0,
                'create_time':create_time
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

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id,
                                               reindent=True, params=params)
        print(self.statement)

    def test_insert_selective(self):
        self.sql_id = 'testInsertSelective'
        params = {'name': 'apple',
                  'category': 'apple',
                  'price': 5.0
                  }

        print("============{}============".format(self.sql_id))
        self.statement = self.mapper.statement(sql_id=self.sql_id,
                                               reindent=True, params=params)
        print(self.statement)


if __name__ == '__main__':
    unittest.main()
