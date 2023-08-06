# -*- utf-8 -*-
import os
import threading

from aestate.exception import LogStatus
from aestate.util import others
from aestate.util.others import write
from aestate.work.Modes import Singleton


class LogCache:
    _instance_lock = threading.RLock()
    # 是否已经显示logo了
    info_logo_show = False
    warn_logo_show = False
    error_logo_show = False
    # 文件名,当满足最大时将会使用一个新的文件作为储存日志
    info_file_name = []
    warn_file_name = []
    error_file_name = []

    def get_filename(self, path, max_clear, status):

        if status == LogStatus.Info:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'
        elif status == LogStatus.Error:
            center_name = 'error'
            oa = self.warn_file_name
            logo_show = 'error_logo_show'
        elif status == LogStatus.Warn:
            center_name = 'warn'
            oa = self.error_file_name
            logo_show = 'warn_logo_show'
        else:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'

        _path = os.path.join(path, center_name)
        if len(oa) == 0:
            oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
            setattr(self, logo_show, False)
        else:
            if not os.path.exists(os.path.join(_path, oa[len(oa) - 1])):
                write(os.path.join(_path, '.temp'), '')
                setattr(self, logo_show, False)
            if os.path.getsize(os.path.join(_path, oa[len(oa) - 1])) >= max_clear:
                oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
                setattr(self, logo_show, False)

        return os.path.join(center_name, oa[len(oa) - 1])

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance
