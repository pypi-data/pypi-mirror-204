# -*- utf-8 -*-
import asyncio
import uuid

from aestate.work.Modes import EX_MODEL
from aestate.work.Serialize import QuerySet
from aestate.work.orm import AOrm


class RepositoryProxy:
    """
    代理仓库的操作方式所有Repository的调用都会经过这里

    这个位置是用来方便使用type对象的Pojo类行为

    通过Repository的__get__方法获得调用时的cls值,使得

    """

    @property
    def conversion(self):
        """
        将此Repository转换为ORM实体

        Return:
            ORM转换之后的实体对象
        """
        return AOrm(repository=self)

    def first(self):
        """
        获取数据库中的第一个
        """
        return self.conversion.top().end()

    def last(self):
        """
        获取最后一个参数
        """
        return self.conversion.top().desc().end()

    def find_all(self, **kwargs) -> QuerySet:
        """
        从当前数据表格中查找所有数据

        Returns:
            将所有结果封装成POJO对象集合并返回数据
        """
        # 开启任务
        self.result = self.find_field(*self.getFields(), **kwargs)
        return self.result

    def find_field(self, *args, **kwargs) -> QuerySet:
        """
        只查询指定名称的字段,如:

            SELECT user_name FROM `user`

            即可参与仅解析user_name为主的POJO对象

        :param args:需要参与解析的字段名

        :return:
            将所有结果封装成POJO对象集合并返回数据

        """
        # 设置名称
        name = str(uuid.uuid1())
        # 开启任务
        kwargs.update(
            {
                'func': self.operation.__find_by_field__,
                '__task_uuid__': name,
                't_local': self
            }
        )

        result = self.operation.start(*args, **kwargs)

        self.result = self.serializer(instance=self, base_data=result)
        return self.result

    def find_one(self, sql, **kwargs):
        """
        查找第一条数据

            可以是一条

            也可以是很多条中的第一条

        code:

            result = self.find_many(**kwargs)
            if len(result) == 0:
                return None
            else:
                return result[0]

        :param kwargs:包含所有参数:

            pojo:参照对象

            sql:处理过并加上%s的sql语句

            params:需要填充的字段

            print_sql:是否打印sql语句

        :return 返回使用find_many()的结果种第一条
        """
        kwargs['sql'] = sql
        self.result = self.find_many(**kwargs)
        if self.result is None or len(self.result) == 0:
            self.result = []
            return None
        else:
            self.result = self.result.first()
            return self.result

    def find_many(self, sql, **kwargs) -> QuerySet:
        """
        查询出多行数据

            第一个必须放置sql语句

        :param kwargs:包含所有参数:

            pojo:参照对象

            sql:处理过并加上%s的sql语句

            params:需要填充的字段

            print_sql:是否打印sql语句

        :return 将所有数据封装成POJO对象并返回

        """
        # 设置名称
        name = str(uuid.uuid1())
        kwargs['sql'] = sql
        # 开启任务
        kwargs['func'] = self.operation.__find_many__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)
        self.__clear_params__()
        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def find_sql(self, sql, **kwargs) -> QuerySet:
        """

        返回多个数据并用list包装:

            - 可自动化操作

            - 请尽量使用find_many(sql)操作

        :param kwargs:包含所有参数:
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        """
        # kwargs['conf_obj'] = t_local.config_obj
        # 设置名称
        name = str(uuid.uuid1())
        kwargs['sql'] = sql
        # 开启任务
        kwargs['func'] = self.operation.__find_sql__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def update(self, key=None):
        """
        执行更新操作:
            返回受影响行数

        :param key:主键，where的参考数据
        :return:
        """
        if key is None:
            for k, v in self._fields.items():
                if hasattr(v, "primary_key") and getattr(v, 'primary_key'):
                    key = k
                    break
        name = str(uuid.uuid1())
        kwargs = {
            'pojo': self,
            'func': self.operation.__update__,
            '__task_uuid__': name,
            't_local': self,
            'key': key
        }
        # 开启任务
        self.result = self.operation.start(**kwargs)
        return self.result

    def remove(self, key=None):
        """
        执行更新操作:
            返回受影响行数

        :param key:主键，where的参考数据
        :return:
        """
        if key is None:
            for k, v in self._fields.items():
                if hasattr(v, "primary_key") and getattr(v, 'primary_key'):
                    key = k
                    break
        name = str(uuid.uuid1())
        kwargs = {
            'pojo': self,
            'func': self.operation.__remove__,
            '__task_uuid__': name,
            't_local': self,
            'key': key
        }
        # 开启任务
        self.result = self.operation.start(**kwargs)
        return self.result

    def save(self, *args, **kwargs):
        """
        将当前储存的值存入数据库
        """
        kwargs['pojo'] = self
        return self.create(*args, **kwargs)

    def create(self, pojo, **kwargs):
        """
        插入属性:
            返回受影响行数
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
        :return:rowcount,last_id if last_id=True
        """
        # 设置名称
        kwargs['pojo'] = pojo
        name = str(uuid.uuid1())
        # 开启任务
        kwargs['func'] = self.operation.__insert__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        self.result = self.operation.start(**kwargs)
        self.__clear_params__()
        return self.result

    def copy(self, *args, **kwargs):
        """
        复制对象进行操做

        不建议多次创建对象，建议使用 pojo.copy()来生成对象
        """
        obj = self.__class__(new=True, *args, **kwargs)
        [setattr(obj, k, v) for k, v in kwargs.items()]
        return obj

    def execute_sql(self, sql, params=None, mode=EX_MODEL.SELECT, **kwargs):
        """
        :param sql:执行的sql
        :param params:防止sql注入的参数
        :param mode:查询模式,默认使用SELECT,使用aestate.work.Modes.EX_MODEL枚举修改执行的sql类型
        :param kwargs:其他需要的参数
        """
        self.__clear_params__()
        d = self.__dict__
        d.update(kwargs)
        kwargs = d
        kwargs['print_sql'] = False if 'print_sql' not in kwargs.keys() else kwargs['print_sql'] if kwargs[
            'print_sql'] else False
        if mode is None or mode == EX_MODEL.SELECT:
            self.result = self.db_util.select(sql=sql, params=params, **kwargs)
        else:
            kwargs['last_id'] = True if 'last_id' not in kwargs.keys() else kwargs['last_id']
            self.result = self.db_util.insert(sql=sql, params=params, **kwargs)
        self.__clear_params__()
        return self.result

    def foreign_key(self, cls, key_name, field_name=None, data=None, operation=None):
        """
        根据外键来查
        :param cls:目标外键的类，注意不是对象，是类
        :param key_name:外键的id
        :param field_name:保存进去的字段名字，默认以表名命名
        :param data:使用已有的数据作为外键
        :param operation:自定义操作
        """
        child_obj = cls()
        if field_name is None:
            name = child_obj.get_tb_name()
        else:
            name = field_name
        self.datas = self.result if data is None else data
        for i in range(len(self.datas)):
            if not operation:
                data = child_obj.orm.filter(**{key_name: self.datas[i].id})
            else:
                data = operation(self.datas, i)
            self.datas[i].add_field(name, data.to_dict())

    def __clear_params__(self):
        """
        清空params参数
        :return:
        """
        if hasattr(self, 'params'):
            self.params.clear()


class RepositoryAsyncProxy(RepositoryProxy):
    """
    代理执行仓库的异步操作,详情请查看SqlOperaProxy类
    """

    def find_all_async(self, *args, **kwargs):
        async def find_all():
            pass

        return asyncio.run(find_all(*args, **kwargs))

    async def find_field_async(self, *args, **kwargs):
        return self.find_field(*args, **kwargs)

    async def find_one_async(self, *args, **kwargs):
        return self.find_one(*args, **kwargs)

    async def find_many_async(self, *args, **kwargs):
        return self.find_many(*args, **kwargs)

    async def find_sql_async(self, *args, **kwargs):
        return self.find_sql(*args, **kwargs)

    async def update_async(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    async def remove_async(self, *args, **kwargs):
        return self.remove(*args, **kwargs)

    async def save_async(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    async def create_async(self, pojo, **kwargs):
        return self.create(pojo, **kwargs)

    async def execute_sql_async(self, sql, params=None, mode=EX_MODEL.SELECT, **kwargs):
        return self.execute_sql(sql=sql, params=params, mode=mode, **kwargs)
