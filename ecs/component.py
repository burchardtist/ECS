from abc import ABC
from uuid import UUID, uuid4

import attr

from ecs.entity import Entity


@attr.s(slots=True)
class IComponent(ABC):
    entity = attr.ib(type=Entity)  # todo: default=None
    id = attr.ib(init=False)

    @id.default
    def _init_id(self) -> UUID:
        return uuid4()
