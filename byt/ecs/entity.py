from uuid import UUID, uuid4

from byt.middleware.component_manager import ComponentManager


class Entity:
    id: UUID
    components: ComponentManager

    def __init__(self) -> None:
        self.id = uuid4()
        self.components = ComponentManager()
