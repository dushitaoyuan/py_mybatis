import pymysql
from DBUtils.PooledDB import PooledDB

mysql_pool = PooledDB(
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

