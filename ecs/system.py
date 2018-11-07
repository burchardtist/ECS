from abc import ABC, abstractmethod


class ISystem(ABC):
    engine = None
    priority = None

    @abstractmethod
    def process(self, *args, **kwargs):
        pass
