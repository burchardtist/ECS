from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from byt.ecs.entity import Entity


@dataclass
class IComponent(ABC):
    entity: Entity
    id: UUID = field(init=False)

    def __post_init__(self):
        self.id = uuid4()

    def __hash__(self):
        return self.id.int

    def __eq__(self, other):
        return self.id == getattr(other, 'id', None)
