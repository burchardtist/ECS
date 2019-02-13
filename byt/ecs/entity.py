from uuid import UUID, uuid4

from byt.middleware.utils import AttrsDict


class Entity:
    id: UUID
    components: AttrsDict

    def __init__(self) -> None:
        self.id = uuid4()
        self.components = AttrsDict()

    def add_component(self, component) -> None:
        if component not in self.components.keys():
            self.components[component] = set()
        self.components[component].add(component)

    def remove_component(self, component) -> None:
        self.components[component].remove(component)
