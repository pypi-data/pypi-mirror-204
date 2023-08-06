from aestate.work.Serialize import QuerySet
from aestate.exception import FieldNotExist
from aestate.dbs import _mysql
from aestate.work.proxy import SqlOperaProxy
from aestate.work.sql import ExecuteSql, ProxyOpera
from aestate.util.Log import ALog


class Repository(SqlOperaProxy.RepositoryAsyncProxy):
    """
    - POJO类
        - 继承该类表名此类为数据库的pojo类
        - 需要配合:@Table(name, msg, **kwargs)使用
    """

    def __init__(self, config_obj=None, instance=None, log_conf=None, close_log=False, serializer=QuerySet, **kwargs):
        """
        通过继承此类将数据表实体化

            实体化之后你可以使用像类似find_one()等操做

            可以调用conversion()方法将其转化为ORM框架常用的样式

            无需担心类型问题，无需担心datetime无法转换
        使用方法:
            #加入Table注解，并标注表名与描述，因考虑使用者后期优化问题，请务必填写MSG参数

            @Table(name="demo_table", msg="demo message")

            #继承Repository并得到相对应的半自动ORM操做
            class TestClass(Repository):
                # 初始化并super配置
                def __init__(self,**kwargs):
                    super(DemoTable, self).__init__(config_obj=ConF(), log_conf={
                        'path': "/log/",
                        'save_flag': True
                    }, **kwargs)

        初始化配置:

            aestate.util.Config.config的配置类,详见:aestate.work.Config.MysqlConfig

        Attributes:
            以下的字段均可覆盖重写

            config_obj:数据源配置类

            log_conf:日志配置工具

            log_obj:日志对象

            close_log:是否关闭日志

            serializer:序列化使用的类,默认使用aestate.work.Serialize.QuerySet

            instance:实例

            __table_name__:表名称

            operation:操作类的实现

            fields:操作的字段

            sqlFields:sql方言

        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serializer:自定义序列化器,默认使用aestate.work.Serialize.QuerySet
        """
        # 以下使用ParseUtil将所有参数替换为可动态修改
        if config_obj is None:
            ALog.log_error(msg="缺少配置类`config_obj`", obj=FieldNotExist, raise_exception=True)
        self.ParseUtil = config_obj
        self.ParseUtil.set_field_compulsory(
            self, key='config_obj', data=kwargs, val=config_obj)
        # 抽象类
        self.ParseUtil.set_field_compulsory(
            obj=self, data=kwargs, key='abst', val=False)
        # 当本类为抽象类时，仅设置所需要的值
        self.ParseUtil.set_field_compulsory(
            self, key='close_log', data=kwargs, val=close_log)
        # 有没有表名
        self.ParseUtil.set_field_compulsory(self, key='__table_name__', data=kwargs,
                                            val=self.__table_name__ if hasattr(self, '__table_name__') else
                                            '"__table_name__" parsing failed')
        # 参照对象
        # 能操作数据库的，但是没有值
        self.ParseUtil.set_field_compulsory(
            self, key='instance', data=kwargs, val=instance)
        # 取得字段的名称
        self.ParseUtil.set_field_compulsory(
            self, key='fields', data=kwargs, val=list(self.instance.getFields().keys()))
        # 获取sql方言配置
        self.ParseUtil.set_field_compulsory(
            self, key='sqlFields', data=self.config_obj.__dict__, val=_mysql.Fields())
        # 当当前类为抽象类时，为类取消初始化数据库配置
        # 最后的执行结果
        self.ParseUtil.set_field_compulsory(
            self, key='result', data=kwargs, val=None)
        self.ParseUtil.set_field_compulsory(self, key='log_obj', data=kwargs,
                                            val=ALog(**log_conf) if log_conf is not None else None)
        self.ParseUtil.set_field_compulsory(
            self, key='serializer', data=kwargs, val=serializer)
        if not self.abst:
            # 操作类
            self.ParseUtil.set_field_compulsory(
                self, key='operation', data=kwargs, val=ProxyOpera.DbOperation())
            # 连接池
            if hasattr(self, 'config_obj') and self.config_obj:
                self.db_util = ExecuteSql.Db_opera(
                    creator=self.ParseUtil.fieldExist(self.config_obj, 'creator', raise_exception=True),
                    POOL=None if 'POOL' not in kwargs.keys() else kwargs['POOL'],
                    **self.ParseUtil.fieldExist(self.config_obj, 'kw', raise_exception=True))
            else:
                ALog.log_error('`config_obj` is missing', AttributeError, LogObject=self.log_obj, raise_exception=True)
