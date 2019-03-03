from uuid import UUID, uuid4

from panek.relations import ManyRelation

from byt.ecs.component import IComponent

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
