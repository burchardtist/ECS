from abc import ABC
from dataclasses import dataclass, field

from uuid import UUID, uuid4

__all__ = [
    'Relation',
    'ManyRelation',
    'OneRelation',
]


@dataclass(frozen=True)
class Relation(ABC):
    to_type: type
    relation_type: str
    id: UUID = field(default_factory=uuid4, init=False)


@dataclass(frozen=True)
class ManyRelation(Relation):
    to_type: type
    relation_type: str = field(default='many', init=False)


@dataclass(frozen=True)
class OneRelation(Relation):
    to_type: type
    frozen: bool = True
    relation_type: str = field(default='one', init=False)
