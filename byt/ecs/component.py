from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from panek.relations import OneRelation

__all__ = [
    'IComponent',
]


@dataclass
class IComponent(ABC):
    _entity: OneRelation = field(init=False)
    _id: UUID = field(init=False)

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        raise ValueError('Use ORM instead of direct setter.')

    def __post_init__(self):
        from byt.ecs.entity import Entity  # todo: resolve cyclic import
        self._id = uuid4()
        self._entity = OneRelation(to_type=Entity)

    def __hash__(self):
        return self._id.int
