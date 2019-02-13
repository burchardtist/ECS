from typing import Iterable, List, Type, TYPE_CHECKING, Union, TypeVar


IComponentType = Type['IComponent']
IComponentTypeList = Iterable[IComponentType]
IComponentUnion = Union[IComponentType, IComponentTypeList]

StringList = List[str]
StringUnion = Union[str, StringList]

IComponentKey = Union[IComponentUnion, StringUnion]


TSuperVisor = Type['Supervisor']
