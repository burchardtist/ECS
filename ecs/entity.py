from typing import Dict, Set, TYPE_CHECKING
from uuid import UUID, uuid4

from supervisor.utils import AttrsDict

if TYPE_CHECKING:
    from ecs.component import IComponent


class Entity:
    id: UUID = None
    components = None  # type: Dict[IComponent, Set[IComponent]]

    def __init__(self) -> None:
        self.id = uuid4()
        self.components = AttrsDict()

    def add_component(self, component) -> None:
        if component not in self.components.keys():
            self.components[component] = set()
        self.components[component].add(component)

    def remove_component(self, component) -> None:
        self.components[component].remove(component)
