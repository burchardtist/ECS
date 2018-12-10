from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from supervisor.supervisor import Supervisor


class ISystem(ABC):
    engine = None  # type: Supervisor
    priority: int = None

    def __init__(self, priority: int=100) -> None:
        self.priority = priority

    def set_engine(self, engine):
        self.engine = engine

    @abstractmethod
    def process(self, *args, **kwargs) -> None:
        pass
