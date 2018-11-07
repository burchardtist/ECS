import collections
from uuid import UUID

import attr
import pytest

from ecs.component import IComponent
from ecs.entity import Entity
from supervisor.supervisor import Supervisor

ENTITIES_COUNT = 5000


@attr.s(slots=True, hash=True)
class Name(IComponent):
    name = attr.ib(type=str)


@attr.s(slots=True, hash=True)
class Position(IComponent):
    x = attr.ib(type=int)
    y = attr.ib(type=int)


@pytest.fixture
def engine():
    return Supervisor()


@pytest.fixture
def populated_engine():
    engine = Supervisor()
    for i in range(1, ENTITIES_COUNT+1):
        entity = engine.create_entity()
        name = Name(name=f'component_{i}', entity=entity)
        position = Position(x=i, y=i+2, entity=entity)
        engine.add_components(entity, [name, position])
    return engine


def test_create_entity(engine):
    entity = engine.create_entity()
    assert isinstance(entity, Entity)
    assert isinstance(entity.id, UUID)
    assert isinstance(entity.components, collections.MutableMapping)
    assert not entity.components


def test_populated_supervisor(populated_engine):
    assert len(populated_engine.entities) == ENTITIES_COUNT
    for value in populated_engine.components.values():
        assert len(value) == ENTITIES_COUNT

    entity_ids = [x for x in populated_engine.entities]
    for entity_id in entity_ids:
        entity = populated_engine.get_entity(entity_id)
        populated_engine.remove_entity(entity)

    assert len(populated_engine.entities) == 0
    for value in populated_engine.components.values():
        assert len(value) == 0
