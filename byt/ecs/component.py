from abc import ABC
from dataclasses import dataclass, field
from typing import Generic
from uuid import UUID, uuid4

from byt.ecs.entity import Entity
from byt.middleware.typing import IComponentTypeVar


@dataclass
class IComponent(Generic[IComponentTypeVar], ABC):
    entity: Entity
    id: UUID = field(init=False)

    def __post_init__(self):
        self.id = uuid4()

    def __hash__(self):
        return self.id.int

    def __eq__(self, other):
        return self.id == getattr(other, 'id', None)
