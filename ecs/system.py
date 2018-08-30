from abc import ABC, abstractmethod


class ISystem(ABC):
    engine = None
    priority = None

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def engine_process(self, *args, **kwargs):
        self.engine.ec_manager.clear_removed_entities()
        self.process(*args, **kwargs)


class SystemManager:
    systems = list()

    def add(self, engine, system_instance, priority):
        system_instance.engine = engine
        system_instance.priority = priority
        self.systems.append(system_instance)
        self.systems.sort(key=lambda x: x.priority, reverse=True)

    def remove(self, system_instance):
        self.systems.remove(system_instance)

    def run_processes(self, *args, **kwargs):
        for system in self.systems:
            system.process(*args, **kwargs)
