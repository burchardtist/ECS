from typing import Dict, List, Optional, Type
from uuid import UUID

import byt.middleware.typing as ic_typing
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.utils import AttrsDict, make_iterable


class Supervisor:
    entities: Dict[UUID, Entity]
    components: AttrsDict
    systems: List[ISystem]

    def __init__(self):
        self.entities = dict()
        self.components = AttrsDict()
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
            if all([entity.components.get(x) for x in components]):
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
        for component, components_set in entity.components.items():
            self.components[component] -= components_set
        del self.entities[entity.id]

    def add_components(self, entity, components: ic_typing.IComponentTypeList):
        components = make_iterable(components)
        for component in components:
            if component not in self.components.keys():
                self.components[component] = set()
            self.components[component].add(component)
            entity.add_component(component)

    def remove_components(self, components):
        components = make_iterable(components)
        for component in components:
            self.components[component].remove(component)
            component.entity.remove_component(component)

    def add_system(self, system: ISystem) -> None:
        system.set_engine(self)
        self.systems.append(system)
        self.systems.sort(key=lambda x: x.priority, reverse=True)

    def remove_system(self, system: Type[ISystem]) -> None:
        self.systems = [x for x in self.systems if not isinstance(x, system)]

    def execute_system(self, system: Type[ISystem], *args, **kwargs) -> None:
        system_instance = next(s for s in self.systems if isinstance(s, system))
        system_instance.process(*args, **kwargs)
