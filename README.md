# py_mybatis

**python 的 mybatis实现,和python的SqlTemplate实现**

## mybatis 语法支持

### 标签支持

- sql,select,update,insert,delete

- include,if,choose,when,otherwise

- trim,where,set,foreach,bind

### 动态语法支持

- #{},${}
- 新增 $f{}函数语法 
- 废弃ognl语法 改为 python语法
### sql 参数支持

参数 目前只支持 dict 类型 名称为params

### 结果映射
暂不支持,查询结果参见pymysql,pymysql.cursors.DictCursor
### 数据库支持
- mysql
**理论上可支持所有sql类型数据库**
## 使用示例
### 基本示例

```xml

```





