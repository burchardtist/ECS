import collections
from typing import Any, Iterable


def make_iterable(obj: Any) -> Iterable:
    if not obj:
        return list()

    if not isinstance(obj, collections.Iterable) or isinstance(obj, str):
        return [obj]
    return obj
