# -*- utf-8 -*-
import inspect

from aestate.work.proxy.SqlOperaProxy import RepositoryProxy


class BaseManager:
    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                # obj = object.__new__(queryset_class)
                func = getattr(self, name)
                return func(self, *args, **kwargs)

            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        new_methods = {}
        for name, method in inspect.getmembers(queryset_class, predicate=inspect.isfunction):
            # Only copy missing methods.
            if hasattr(cls, name):
                continue
            # Copy the method onto the manager.
            new_methods[name] = create_method(name, method)
        return new_methods

    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        ms = cls._get_queryset_methods(queryset_class)
        return type(class_name, (cls,), {
            'model_class': queryset_class,
            **ms
        })


class ModelBase(BaseManager.from_queryset(RepositoryProxy)):
    def __new__(cls, class_name, class_parent, class_attr):
        return type(class_name, class_parent, class_attr)
