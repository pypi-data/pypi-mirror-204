# Standard library imports
import typing

__all__ = [
    "StructLikeREPR",
    "classproperty",
]


class ClassPropertyDescriptor(object):
    @typing.no_type_check  # todo: remove this
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    @typing.no_type_check  # todo: remove this
    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    @typing.no_type_check  # todo: remove this
    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    @typing.no_type_check  # todo: remove this
    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


@typing.no_type_check  # todo: remove this
def classproperty(func):
    """
    decorator to define a class level property
    """

    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


class ClassPropertyMetaClass(type):
    @typing.no_type_check  # todo: remove this
    def __setattr__(self, key, value):
        if key in self.__dict__:
            obj = self.__dict__.get(key)
        if obj and type(obj) is ClassPropertyDescriptor:
            return obj.__set__(self, value)

        return super(ClassPropertyMetaClass, self).__setattr__(key, value)


class MetaStructLikeREPR(ClassPropertyMetaClass):
    @classmethod
    @typing.no_type_check  # todo: remove this
    def __prepare__(self, name, bases):
        # Standard library imports
        import collections

        return collections.OrderedDict()

    @typing.no_type_check  # todo: remove this
    def __new__(self, name, bases, classdict):
        classdict["__ordered__"] = [
            key
            for key in classdict.keys()
            if not (key.startswith("__") and key.endswith("__"))
        ]
        return type.__new__(self, name, bases, classdict)

    @typing.no_type_check  # todo: remove this
    def __unicode__(cls):
        atts = cls.__ordered__
        result = f"{cls.__name__}("
        if len(atts) > 3:
            longest_key = len(max(atts, key=len))
            result += "\n  "
            result += "\n  ".join(
                f"{att.ljust(longest_key)}: {getattr(cls, att)}" for att in atts
            )
            result += "\n"
        else:
            result += ", ".join(f"{att}: {getattr(cls, att)}" for att in atts)

        result += ")"
        return str(result)

    @typing.no_type_check  # todo: remove this
    def __str__(cls):
        return cls.__unicode__()

    @typing.no_type_check  # todo: remove this
    def __repr__(cls):
        return cls.__unicode__()


class StructLikeREPR(metaclass=MetaStructLikeREPR):
    """ "
    Todo: add docs
    """

    pass
