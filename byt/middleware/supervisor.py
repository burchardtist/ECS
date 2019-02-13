from typing import Dict, List, Optional, Type
from uuid import UUID

import byt.middleware.typing as ic_typing
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.component_manager import ComponentManager
from byt.middleware.utils import make_iterable


class Supervisor:
    entities: Dict[UUID, Entity]
    component_manager: ComponentManager
    systems: List[ISystem]

    def __init__(self):
        self.entities = dict()
        self.component_manager = ComponentManager()
        self.systems = list()

    def get_entity(self, entity_id: UUID) -> Entity:
        return self.entities[entity_id]

    def get_components_intersection(
            self,
            components: ic_typing.IComponentKey
    ) -> List[Entity]:
        result = list()
        components = make_iterable(components)
        for entity in self.entities.values():
            if entity.components.has_all(components):
                result.append(entity)
        return result

    def create_entity(
            self,
            components: Optional[ic_typing.IComponentTypeList] = None
    ) -> Entity:
        entity = Entity()
        self.entities[entity.id] = entity

        if components:
            self.add_components(entity, components)

        return entity

    def remove_entity(self, entity: Entity):
        entity_components = entity.components.get_all()
        self.component_manager.bulk_remove(entity_components)
        del self.entities[entity.id]

    def add_components(self, entity, components: ic_typing.IComponentTypeList):
        components = make_iterable(components)
        for component in components:
            self.component_manager.add(component)
            self._entity_add_component(entity, component)

    def remove_components(self, components) -> None:
        components = make_iterable(components)
        for component in components:
            self.component_manager.remove(component)
            component.entity.components.remove(component)

    def _entity_add_component(self, entity, component):
        entity.components.add(component)

    def add_system(self, system: ISystem) -> None:
        self.systems.append(system)
        self.systems.sort(key=lambda x: x.priority, reverse=True)

    def remove_system(self, system: Type[ISystem]) -> None:
        self.systems = [x for x in self.systems if not isinstance(x, system)]

    def execute_system(self, system: Type[ISystem], *args, **kwargs) -> None:
        system_instance = next(s for s in self.systems if isinstance(s, system))
        system_instance.process(engine=self, *args, **kwargs)
