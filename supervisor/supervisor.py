from typing import Dict, Iterable, List, Set, Type, Union
from uuid import UUID

from ecs.component import IComponent
from ecs.entity import Entity
from ecs.system import ISystem
from supervisor.utils import AttrsDict, make_iterable


class Supervisor:
    entities: Dict[UUID, Entity] = None
    components: Dict[IComponent, Set[IComponent]] = None
    systems: List[ISystem] = None

    def __init__(self):
        self.entities = dict()
        self.components = AttrsDict()
        self.systems = list()

    def get_entity(self, entity_id: UUID) -> Entity:
        return self.entities[entity_id]

    def get_components_intersection(
            self,
            components: Union[IComponent, List[IComponent], str, List[str]]
    ) -> List[Entity]:
        result = list()
        components = make_iterable(components)
        for entity in self.entities.values():
            if all([entity.components.get(x) for x in components]):
                result.append(entity)
        return result

    def create_entity(
            self,
            components: Union[IComponent, Iterable[IComponent]] = None
    ) -> Entity:
        entity = Entity()
        self.entities[entity.id] = entity
        self.add_components(entity, components)
        return entity

    def remove_entity(self, entity: Entity):
        for component, components_set in entity.components.items():
            self.components[component] -= components_set
        del self.entities[entity.id]

    def add_components(self, entity, components: Union[IComponent, Iterable[IComponent]]):
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
