from functools import singledispatch
from typing import Collection, List, TypeVar

T = TypeVar('T')


@singledispatch
def make_iterable(obj: T) -> List[T]:
    return [obj]


@make_iterable.register
def _none(obj: None) -> List:
    return list()


@make_iterable.register(list)
@make_iterable.register(set)
@make_iterable.register(tuple)
def _iterable(obj) -> Collection[T]:
    return obj
