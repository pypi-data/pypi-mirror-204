import threading

from aestate.work.Modes import Singleton


class AestateLanguage:
    LANG = 0x804


class I18n:
    """
    国际化语言,在统一配置下的全局语言解决方案
    """

    def __init__(self, langs=None):
        if langs is None:
            langs = {}
        self.langs = {}
        self.langs.update(langs)

    _instance_lock = threading.RLock()

    def whileGet(self, next_names: list):
        """
        重复获取i18n的字典语句
        :return:
        """
        pass

    def t(self, name: str):
        if AestateLanguage.LANG not in self.langs.keys():
            AestateLanguage.LANG = 0x409
        if name not in self.langs.get(AestateLanguage.LANG).keys():
            raise Exception(f'i18n field is not exist:{name}')
            # return name
        return self.langs.get(AestateLanguage.LANG).get(name)

    def __new__(cls, *args, **kwargs):
        """
        单例管理缓存内容
        """
        instance = Singleton.createObject(cls)
        return instance


class ExceptionI18n(I18n):
    """

    """

    def __init__(self):
        super(ExceptionI18n, self).__init__(langs={
            # 中文(简体,中国)
            0x804: {
                '': '未知错误',
                'if_tag_not_test': 'if 标记中的属性`test` 缺少必需的结构',
                'xml_syntax_error': 'xml语法错误,不相等的逻辑运算符数量,在:%s',
                'before_else_not_if': '在 else 标签前面找不到 if 标签',
                'not_field_name': '被调用的方法中不存在名为 `%s` 的参数',
                'not_from_node_name': '无法从节点中找到名为 `%s` 的模板',
                'not_result_map': "找不到 resultMap 模板",
                "not_type": "无法从节点中找到名为 `type` 的属性",
                "module_not_found": "模块未找到",
            },
            # 英语
            0x409: {
                '': 'Unknow error',
                'if_tag_not_test': 'The attribute`test` in the if tag is missing a required structure',
                'xml_syntax_error': 'Xml syntax error, unequal number of logical operators, from:%s',
                'before_else_not_if': 'Cannot find the if tag in front of the else tag',
                'not_field_name': 'The parameter named `%s` does not exist in the called method',
                'not_from_node_name': 'The template named `%s` could not be found from the node',
                'not_result_map': "Can't find resultMap template",
                "not_type": "The attribute named `type` could not be found from the node",
                "module_not_found": "`%s` Module Not Found",
            },
        })

    @staticmethod
    def tt(name):
        return ExceptionI18n().t(name)


class InfoI18n(I18n):
    """
    提示语句国际化
    """

    def __init__(self):
        super(InfoI18n, self).__init__(langs={
            # 中文(简体,中国)
            0x804: {
                "statement": "执行语句",
                "parameters": "参数",
                "selectResult": "行数",
                "updateResult": "受影响行",
            },
            0x409: {
                "statement": "Statement",
                "parameters": "Parameters",
                "selectResult": "Total",
                "updateResult": "Updates",
            }
        })

    @staticmethod
    def tt(name):
        return InfoI18n().t(name)
