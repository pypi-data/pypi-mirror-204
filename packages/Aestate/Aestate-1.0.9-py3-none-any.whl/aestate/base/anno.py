from aestate.base.model import Model
from aestate.work.Manage import Pojo


def Table(name, msg="", **kwargs):
    """
        标注该类为一个表
        :param name:表的名称
        :param msg:表的描述
        :return:
        """

    def set_to_field(cls: Model):
        dbtype = cls.Config.dbtype(cls.Config.creator)
        pojo = Pojo(config_obj=dbtype, log_conf=cls.Log.__dict__)
        setattr(cls, '__table_name__', name)
        setattr(cls, '__table_msg__', msg)
        cls.instance = pojo
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls

    return set_to_field
