from ecs.entity_component import EntityComponentManager
from ecs.system import SystemManager


class Engine:
    ec_manager = EntityComponentManager()
    system_manager = SystemManager()

    # ENTITY
    def create_entity(self):
        return self.ec_manager.create_entity()

    def remove_entity(self, entity, immediate=False):
        return self.ec_manager.remove_entity(entity, immediate)

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
        self.system_manager.run_processes(*args, **kwargs)
