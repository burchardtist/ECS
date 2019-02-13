from abc import ABC, abstractmethod


class ISystem(ABC):
    priority: int

    def __init__(self, priority: int=100) -> None:
        self.priority = priority

    @abstractmethod
    def process(self, engine, *args, **kwargs) -> None:
        pass
