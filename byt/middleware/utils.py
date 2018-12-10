import collections
from typing import Any, Iterable


def make_iterable(obj: Any) -> Iterable:
    if not obj:
        return list()

    if not isinstance(obj, collections.Iterable) or isinstance(obj, str):
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
