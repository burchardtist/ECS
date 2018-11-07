import collections
from typing import Any, Iterable


def make_iterable(obj: Any) -> Iterable:
    if not obj:
        return list()

    if not isinstance(obj, collections.Iterable):
        return [obj]
    return obj


class AttrsDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        if not isinstance(key, str):
            key = key.__class__.__name__
        return key
# class AttrsDict(dict):
#     def __setitem__(self, key, item):
#         if not isinstance(key, str):
#             key = key.__class__.__name__
#         self.__dict__[key] = item
#
#     def __getitem__(self, key):
#         if not isinstance(key, str):
#             key = key.__class__.__name__
#         return self.__dict__[key]
#
#     def __delitem__(self, key):
#         if not isinstance(key, str):
#             key = key.__class__.__name__
#         del self.__dict__[key]
#
#     def __repr__(self):
#         return repr(self.__dict__)
#
#     def __len__(self):
#         return len(self.__dict__)
#
#     def clear(self):
#         return self.__dict__.clear()
#
#     def copy(self):
#         return self.__dict__.copy()
#
#     def has_key(self, key):
#         return key.__class__.__name__ in self.__dict__
#
#     def update(self, *args, **kwargs):
#         return self.__dict__.update(*args, **kwargs)
#
#     def keys(self):
#         return self.__dict__.keys()
#
#     def values(self):
#         return self.__dict__.values()
#
#     def items(self):
#         return self.__dict__.items()
#
#     def pop(self, *args):
#         return self.__dict__.pop(*args)
#
#     def get(self, key, default=None):
#         if not isinstance(key, str):
#             key = key.__class__.__name__
#         try:
#             return self.__dict__[key]
#         except KeyError:
#             return default
#
#     def __cmp__(self, dict_):
#         return self.__cmp__(self.__dict__, dict_)
#
#     def __contains__(self, item):
#         return item.__class__.__name__ in self.__dict__
#
#     def __iter__(self):
#         return iter(self.__dict__)
