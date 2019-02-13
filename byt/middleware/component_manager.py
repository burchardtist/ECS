import collections
from typing import Union, Set, Mapping, List, Iterable

__all__ = [
    'ComponentManager'
]


class TypeKeyDict(collections.MutableMapping):
    """Set key as name of class, object's class or str.
    """
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

    def __keytransform__(self, key: Union[type, str, object]) -> str:
        if isinstance(key, type):
            return key.__name__
        if not isinstance(key, str):
            return key.__class__.__name__
        return key


class ComponentManager:
    _components: TypeKeyDict

    def __init__(self):
        self._components = TypeKeyDict()

    def add(self, component):  # IComponent
        components_container = self._components
        if component not in components_container.keys():
            components_container[component] = set()
        components_container[component].add(component)

    def remove(self, component):  # IComponent
        self._components[component].remove(component)

    def bulk_remove(self, components_map):
        for key, value in components_map:
            self._components[key] -= value

    def get_all(self):
        return self._components.items()

    def has_all(self, components: Iterable):  # IComponents
        return all([self._components.get(x) for x in components])

    def get_group(self, key):
        for obj in self._components[key]:
            yield obj

    def group_len(self, key) -> int:
        if key not in self._components.keys():
            return 0
        return sum(1 for _ in self._components[key])
