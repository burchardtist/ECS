from uuid import UUID, uuid4

from byt.ecs.component import IComponent
from byt.object_relations.relations import ManyRelation

__all__ = [
    'Entity',
]


class Entity:
    def __init__(self) -> None:
        self.id: UUID = uuid4()
        self._components: ManyRelation = ManyRelation(to_type=IComponent)

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, value):
        raise ValueError('Use ORM instead of direct setter.')
