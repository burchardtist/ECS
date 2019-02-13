from typing import Iterable, List, Type, Union

IComponentType = Type['IComponent']
IComponentTypeList = Iterable[IComponentType]
IComponentUnion = Union[IComponentType, IComponentTypeList]

StringList = List[str]
StringUnion = Union[str, StringList]

IComponentKey = Union[IComponentUnion, StringUnion]
