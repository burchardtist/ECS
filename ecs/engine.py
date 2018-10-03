from ecs.entity_component import EntityComponentManager
from ecs.system import SystemManager


class Engine:
    ec_manager = EntityComponentManager()
    system_manager = SystemManager()
    context = dict()

    # ENTITY
    def create_entity(self):
        return self.ec_manager.create_entity()

    def remove_entity(self, entity, immediate=False):
        return self.ec_manager.remove_entity(entity, immediate)

    def get_entity_components(self, entity):
        return self.ec_manager.get_entity_components(entity)

    # COMPONENT
    def add_component(self, entity, component):
        self.ec_manager.add_components(entity, component)

    def remove_component(self, entity, component_type):
        self.ec_manager.remove_components(entity, component_type)

    def get_components(self, component_types):
        return self.ec_manager.get_components(component_types)

    # SYSTEM
    def add_system(self, system_instance, priority=0):
        self.system_manager.add(self, system_instance, priority)

    def process(self, *args, **kwargs):
        self.ec_manager.clear_removed_entities()
        self.system_manager.run_processes(*args, **kwargs)

    # CONTEXT
    def get_context_item(self, key):
        try:
            return self.context[key]
        except KeyError:
            return
