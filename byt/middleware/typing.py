from typing import Iterable, List, Type, TypeVar, Union

IComponentTypeVar = TypeVar('IComponentTypeVar')

IComponentType = Type[IComponentTypeVar]
IComponentTypeList = Iterable[IComponentType]
IComponentUnion = Union[IComponentType, IComponentTypeList]

StringList = List[str]
StringUnion = Union[str, StringList]

IComponentKey = Union[IComponentUnion, StringUnion]
