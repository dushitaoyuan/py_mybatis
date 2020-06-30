# py_mybatis

- python的mybatis实现
- python的SqlTemplate实现



## 项目起源

**特别鸣谢**:<a href='https://github.com/hhyo/mybatis-mapper2sql'>mybatis-mapper2sql </a>

**借助这位大佬使我快速实现了py_mybatis,mapper xml解析主体代码都是 hhyo大佬的**

本人是位javaer,刚刚开始学习python,当开始学习数据库相关api时,发现python中并未有很好的开发包,

重型orm 直接淘汰,不要问为什么,问就是我喜欢写sql,虽然sql写的不咋的

急需一种轻型的,开箱即用的类似mybatis的开发包,找了半天也没有,算了,不如自己造轮子,这个念头一直在我心中萦绕

无奈,python刚学没多久,稍微有些难度,时间也不太充足,直到遇到了mybatis-mapper2sql,才成为可能,感谢大佬



**特别提醒**

暂未发布开发包,只能下载使用

私以为未经过测试就发布,容易挨骂,所以等等看,看看反馈吧



## mybatis 语法支持

### 标签支持

- sql,select,update,insert,delete

- include,if,choose,when,otherwise

- trim,where,set,foreach,bind

### 动态语法支持

- #{},${}
- 新增 $f{}函数语法 ,允许开发者自行注册函数,参见:mapper_func.py
- 废弃ognl语法 改为 python语法
- 参数转换(核心代码在type_handler.py)
### sql 参数支持

参数 目前只支持 dict 类型 名称为params

### 结果映射
暂不支持,查询结果参见pymysql,pymysql.cursors.DictCursor
### 数据库支持
- mysql
**理论上可支持所有sql类型数据库**
## 使用示例
### 基本示例

**测试表结构**

```sql

```



####  PdbcSqlTemplate(sql模板用法)

**参见:tests/sql_template_test.py**

```python
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
            host="localhost",
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

```

#### MybatisSqlSession 使用

- mapper.xml

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
  <mapper namespace="Test">
      <sql id="sometable">
          fruits
      </sql>
      <sql id="somewhere">
          WHERE
          category = #{category}
      </sql>
      <sql id="someinclude">
          FROM
          <include refid="${include_target}"/>
          <include refid="somewhere"/>
      </sql>
  
  
      <delete id="deleteById">
          delete from fruits where id =#{id}
      </delete>
      <select id="testBasic">
          SELECT
          id,
          name,
          category,
          price
          FROM
          fruits
          WHERE
          category = 'apple' AND
          <![CDATA[ price < 500 ]]>
      </select>
  
      <select id="test_function">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          WHERE
          category =$f{like(params['name'])}
          and create_time =$f{time_format(params['create_time'])}
      </select>
      <select id="testParameters">
          SELECT
          id,
          name,
          category,
          price
          FROM
          fruits
          WHERE
          category = #{category,sql_type=VARCHAR}
          AND price > ${price,sql_type=BIGINT}
          AND type = ${type,sql_type=BOOLEAN}
      </select>
      <select id="testInclude">
          SELECT
          name,
          category,
          price
          <include refid="someinclude">
              <property name="prefix" value="Some"/>
              <property name="include_target" value="sometable"/>
          </include>
      </select>
      <select id="testIf">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          WHERE
          1=1
          <if test="'category' in params">
              AND category = #{category}
          </if>
          <if test="'price' in params">
              AND price = ${price}
              <if test="params['price'] >= 400">
                  AND name = 'pear'
              </if>
          </if>
      </select>
  
      <select id="testTrim">
          SELECT
          name,
          category,
          price
          FROM
          fruits
  
          <trim prefix="WHERE" prefixOverrides="OR">
              OR category = 'apple'
              OR price = 200
          </trim>
          <trim prefix="AND" prefixOverrides="OR">
              (type = 1 OR type= 0)
          </trim>
      </select>
      <select id="testWhere">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          <where>
              AND category = 'apple'
              <if test="'price' in params ">
                  AND price = ${price}
              </if>
          </where>
      </select>
      <update id="testSet">
          UPDATE
          fruits
          <set>
              <if test="'category' in params">
                  category = #{category},
              </if>
              <if test="'price' in params">
                  price = ${price}
              </if>
          </set>
          WHERE
          name = #{name}
      </update>
      <select id="testChoose">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          <where>
              <choose>
                  <when test="'name' in params">
                      AND name = #{name}
                  </when>
                  <when test="'category' in params and  params['category'] == 'banana'">
                      AND category = #{category}
                      <if test="'price' in params">
                          AND price = ${price}
                      </if>
                  </when>
                  <otherwise>
                      AND category = 'apple'
                  </otherwise>
              </choose>
          </where>
      </select>
      <select id="testForeach">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          <where>
              category = 'apple' AND name in
              <foreach collection="names" item="name" open="(" close=")" separator=",">
                  #{name}
              </foreach>
          </where>
      </select>
      <insert id="testInsertMulti">
          INSERT INTO
          fruits
          (
          id,
          name,
          category,
          price,
          create_time
          )
          VALUES
          <foreach collection="fruits" item="fruit" separator=",">
              (
              #{fruit['id']},
              #{fruit['name']},
              #{fruit['category']},
              #{fruit['price']},
              $f{time_format(fruit['create_time'])}
  
              )
          </foreach>
      </insert>
      <select id="testBind">
          <bind name="likeName" value="'%{}%'.format(params['name'])"/>
          SELECT
          name,
          category,
          price
          FROM
          fruits
          WHERE
          name like #{likeName}
      </select>
      <insert id="testInsertSelective">
          insert into fruits
          <trim prefix="(" suffix=")" suffixOverrides=",">
              <if test="'name' in params">
                  name,
              </if>
              <if test="'category' in params">
                  category,
              </if>
              <if test="'price' in params">
                  price,
              </if>
          </trim>
          <trim prefix="values (" suffix=")" suffixOverrides=",">
              <if test="'name' in params">
                  #{name},
              </if>
              <if test="'category' in params">
                  #{category},
              </if>
              <if test="'category' in params">
                  #{price},
              </if>
          </trim>
      </insert>
      <select id="testChooseNative">
          SELECT
          name,
          category,
          price
          FROM
          fruits
          <where>
              <choose>
                  <when test="'name' in params">
                      AND name = #{name}
                  </when>
                  <when test="'category' in params and params['category'] == 'banana'">
                      AND category = #{category}
                      <if test="'price' in params">
                          AND price = ${price}
                      </if>
                  </when>
                  <otherwise>
                      AND category = 'apple'
                  </otherwise>
              </choose>
          </where>
      </select>
  
      <insert id="insertOne">
          insert into fruits(id,name,category,price) values(#{id},#{name},#{category},#{price})
      </insert>
  </mapper>
  
  ```

- 示例代码

```python
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
        params = {'name': 'apple',
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

```




