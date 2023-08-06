import re
import sys

from aestate.exception import BaseSqlError
from aestate.i18n import InfoI18n
from aestate.util.Log import ALog
from dbutils.pooled_db import PooledDB


def parse_kwa(db, **kwargs):
    """
    解析并执行sql

    :param db:db_util对象
    :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
            many:是否有多个
    """

    try:
        cursor = db.cursor()
        # 是否执行多条sql
        sql = kwargs['sql']
        params = kwargs['params'] if 'params' in kwargs.keys() else None
        many_flay = 'many' in kwargs.keys() and kwargs['many']
        if ('print_sql' in kwargs.keys() and kwargs['print_sql'] is True) or (kwargs['config_obj'].print_sql is True):
            _l = sys._getframe().f_back.f_lineno
            # 输出sql
            msg = InfoI18n.tt("statement") + ' ==> ' + (f'{sql} - many=True' if many_flay else sql)
            ALog.log(obj=db, line=_l, task_name='ASQL', msg=msg,
                     LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None)
            # 输出字段
            output_params = params if params else ()
            parameters = InfoI18n.tt("parameters") + " ==> "
            for i in output_params:
                parameters += ' {}{},'.format(str(i), re.findall('<class \'(.*)\'>', str(type(i))))
            if parameters[-1] == ',':
                parameters = parameters[:-1]
            ALog.log(obj=db, line=_l, task_name='ASQL', msg=parameters,
                     LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None)

        if many_flay:
            cursor.executemany(sql,
                               tuple(params) if params else ())
        else:
            if params:
                cursor.execute(sql, tuple(params))
            else:
                cursor.execute(sql)
            # try:
            #     CACodeLog.log(obj=db, line=_l, task_name='Print Sql', msg=cursor._executed)
            # except:
            #     CACodeLog.log(obj=db, line=_l, task_name='Print Sql', msg=msg)
        return cursor
    except Exception as e:
        db.rollback()
        mysql_err = BaseSqlError(e)
        mysql_err.raise_exception()


class Db_opera(PooledDB):
    def __init__(self, *args, **kwargs):
        if 'POOL' not in kwargs or kwargs['POOL'] is None:
            self.POOL = self
        if 'POOL' in kwargs.keys():
            kwargs.pop('POOL')

        super(Db_opera, self).__init__(*args, **kwargs)

    def get_conn(self):
        """
        获取数据库连接池
        :return:
        """
        conn = self.POOL.connection()
        return conn

    def select(self, **kwargs):
        """
        查找多个
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        :return:
        """
        db = self.get_conn()
        _l = sys._getframe().f_back.f_lineno
        try:
            cursor = parse_kwa(db=db, **kwargs)
            # 列名
            col = cursor.description
            data = cursor.fetchall()
            _result = []
            for data_index, data_value in enumerate(data):
                _messy = {}
                for item_index, item_value in enumerate(data_value):
                    _messy[col[item_index][0]] = item_value
                _result.append(_messy)
            # 缓存
            # if scm.status == CacheStatus.OPEN:
            #     scm.set(sql=sql, value=_result, instance=kwargs['instance'] if 'instance' in kwargs.keys() else None)

            msg = InfoI18n.tt("selectResult") + ' ==> ' + (str(len(_result)) if _result is not None else '0')
            ALog.log(obj=db, line=_l, task_name='ASQL', msg=msg,
                     LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None)
            db.close()
            return _result
        except Exception as e:
            db.rollback()
            ALog.log_error(msg=str(e), obj=e,
                           LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None,
                           raise_exception=True)
        finally:
            db.close()

    def insert(self, many=False, **kwargs):
        """
        执行插入语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :param many:是否为多行执行
        """
        db = self.get_conn()
        _l = sys._getframe().f_back.f_lineno
        try:
            cursor = parse_kwa(db=db, many=many, **kwargs)
            db.commit()
            # 受影响行数
            rowcount = cursor.rowcount
            msg = InfoI18n.tt("updateResult") + ' ==> ' + str(rowcount)
            ALog.log(obj=db, line=_l, task_name='ASQL', msg=msg,
                     LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None)
            # 返回受影响行数
            if kwargs['last_id']:
                return rowcount, cursor.lastrowid
            else:
                return rowcount
        except Exception as e:
            db.rollback()
            ALog.log_error(msg=str(e), obj=e,
                           LogObject=kwargs['log_obj'] if 'log_obj' in kwargs.keys() else None,
                           raise_exception=True)
        finally:
            db.close()

    def update(self, **kwargs):
        """
        执行更新语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        return self.insert(**kwargs)

    def delete(self, **kwargs):
        """
        执行删除语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        self.insert(**kwargs)
