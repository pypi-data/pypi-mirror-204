import enum

from aestate.base.manage import BaseManager
from aestate.dbs import mysql
from aestate.work.Adapter import LanguageAdapter
from aestate.work.Manage import Pojo

base_dict = ['__module__', '__dict__', '__weakref__', '__doc__']


class Model(BaseManager.from_queryset(Pojo)):
    class Log(enum.Enum):
        enable = False
        path = None
        max_clear = 10

    class Config(enum.Enum):
        dbtype = None
        creator = None
        print_sql = True
        last_id = True
        adapter = LanguageAdapter

    class Database(enum.Enum):
        # 数据库地址
        host = None
        # 数据库端口
        port = 3306,
        # 数据库名
        database = None
        # 数据库用户
        user = None
        # 数据库密码
        password = None
        # 数据库创建者，如果你用的是mysql，那么这里就是pymysql，如果用的是sqlserver，那么这里就应该是pymssql
        db_type = None

    name = ""

    class Operas:
        pass
