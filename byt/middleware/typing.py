from typing import Iterable, Union

from byt.ecs.component import IComponent

__all__ = [
    'IterableIComponent',
    'IComponentKey',
]


IterableIComponent = Iterable[IComponent]
IComponentKey = Union[IComponent, IterableIComponent]
