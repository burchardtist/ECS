from abc import ABC, abstractmethod
from typing import Optional

from byt.middleware.typing import TSuperVisor


class ISystem(ABC):
    engine: Optional[TSuperVisor]
    priority: int

    def __init__(self, priority: int=100) -> None:
        self.priority = priority

    def set_engine(self, engine: TSuperVisor) -> None:
        self.engine = engine

    @abstractmethod
    def process(self, *args, **kwargs) -> None:
        pass
