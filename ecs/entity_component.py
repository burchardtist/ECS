import collections
from functools import wraps, reduce
from typing import Dict
from uuid import uuid4, UUID


def update_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._update = True
        return result
    return wrapper


class EntityComponentManager:
    _entities = dict()
    components = dict()
    dead_entities = list()
    _update = True

    @property
    def entities(self):
        if self._update:
            self._entities = self._get_entities()
        return self._entities

    def _get_entities(self):
        result: Dict[UUID, Dict[str, object]] = dict()
        for type_, entities in self.components.items():
            for entity, object_ in entities.items():
                try:
                    result[entity][type_] = object_
                except KeyError:
                    result[entity] = dict()
                    result[entity][type_] = object_
        self._update = False
        return result

    @update_required
    def create_entity(self):
        entity = uuid4()
        return entity

    def remove_entity(self, entity, immediate=False):
        (self._remove_entity(entity)
         if immediate
         else self.dead_entities.append(entity))

    def clear_removed_entities(self):
        for entity in self.dead_entities:
            self._remove_entity(entity)
        self.dead_entities = list()

    @update_required
    def _remove_entity(self, entity):
        components_types = self.entities[entity].keys()
        self.remove_components(entity, components_types)

    @update_required
    def add_components(self, entity, component_instances):
        if not isinstance(component_instances, collections.Iterable):
            component_instances = [component_instances]

        for component_instance in component_instances:
            component_type = type(component_instance)
            if component_type not in self.components.keys():
                self.components[component_type] = dict()
            self.components[component_type][entity] = component_instance

    @update_required
    def remove_components(self, entity, component_types):
        if not isinstance(component_types, collections.Iterable):
            component_types = [component_types]
        for component_type in component_types:
            del self.components[component_type][entity]
            if not self.components[component_type]:
                del self.components[component_type]

    def get_components(self, component_types):
        if not isinstance(component_types, collections.Iterable):
            component_types = {component_types}

        component_containers = [self.components[ct] for ct in component_types]
        entities = reduce(
            lambda acc, x: [element for element in acc if element in x],
            component_containers)
        for entity in entities:
            yield (entity, *[self.entities[entity][x] for x in component_types])
