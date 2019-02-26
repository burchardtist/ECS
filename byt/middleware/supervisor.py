from typing import Dict, List, Set, Type
from uuid import UUID

import byt.middleware.typing as t
from byt.ecs.component import IComponent
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.utils import make_iterable
from byt.object_relations.control import ObjectRelationManager


class Supervisor:
    def __init__(self):
        self.entities: Dict[UUID, Entity] = dict()
        self.systems: List[ISystem] = list()
        self.orm: ObjectRelationManager = ObjectRelationManager()

    def get_entity(self, entity_id: UUID) -> Entity:
        return self.entities[entity_id]

    def get_components_intersection(
            self,
            components: t.IComponentKey
    ) -> Set[Entity]:
        components = make_iterable(components)
        entity_sets = list()
        for component_type in components:
            component_objects = self.orm.get_type(component_type)
            entity_set = {
                self.orm.get_relation(c.entity) for c in component_objects
            }
            entity_sets.append(entity_set)
        return set.intersection(*entity_sets)

    def create_entity(self) -> Entity:
        entity = Entity()
        self.entities[entity.id] = entity
        return entity

    def remove_entity(self, entity: Entity):
        entity_components = self.orm.get_relation(entity.components)
        if entity_components:
            self.remove_components(entity_components.copy())
        del self.entities[entity.id]

    def get_entity_components(self, entity: Entity) -> Dict[Type, Set[IComponent]]:
        components = self.orm.get_relation(entity.components) or list()
        result = dict()
        for component in components:
            component_type = type(component)
            if component_type not in result.keys():
                result[component_type] = set()
            result[component_type].add(component)
        return result

    def get_components(self, component: Type[IComponent]) -> Set[IComponent]:
        return self.orm.get_type(component)

    def get_component_entity(self, component: IComponent) -> Set[Entity]:
        return self.orm.get_relation(component.entity)

    def add_components(self, entity, components: t.IterableIComponent):
        components = make_iterable(components)
        for component in components:
            self.orm.add(entity, component)

    def remove_components(self, components) -> None:
        components = make_iterable(components)
        for component in components:
            # todo: ObjectRelation powinien sam wyciągnąć te entity i je sobie usunąć na poziomie relacji
            entity = self.orm.get_relation(component.entity)
            self.orm.remove(component, entity)

    def add_system(self, system: ISystem) -> None:
        self.systems.append(system)
        self.systems.sort(key=lambda x: x.priority, reverse=True)

    def remove_system(self, system: Type[ISystem]) -> None:
        self.systems = [x for x in self.systems if not isinstance(x, system)]

    def execute_system(self, system: Type[ISystem], *args, **kwargs) -> None:
        system_instance = next(s for s in self.systems if isinstance(s, system))
        system_instance.process(engine=self, *args, **kwargs)
