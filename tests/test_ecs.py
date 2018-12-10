import collections
from uuid import UUID

import attr
import pytest

from byt.ecs.component import IComponent
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.supervisor import Supervisor

ENTITIES_COUNT = 5000
TEST_NAME = 'NameSystemTest'


# COMPONENTS
@attr.s(slots=True, hash=True)
class Name(IComponent):
    name = attr.ib(type=str)


@attr.s(slots=True, hash=True)
class Position(IComponent):
    x = attr.ib(type=int)
    y = attr.ib(type=int)


@attr.s(slots=True, hash=True)
class FooBar(IComponent):
    foo = attr.ib(type=bool)
    bar = attr.ib(type=bool)


# SYSTEMS
class PositionSystem(ISystem):
    def process(self, *args, **kwargs):
        position_entities = self.engine.get_components_intersection('Position')
        for entity in position_entities:
            for position in entity.components['Position']:
                position.x += 1
                position.y += 1


class NameSystem(ISystem):
    def process(self, *args, **kwargs):
        name_entities = self.engine.get_components_intersection('Name')
        for entity in name_entities:
            for name in entity.components['Name']:
                name.name = TEST_NAME


# FIXTURES
@pytest.fixture
def engine():
    engine = Supervisor()
    return engine


@pytest.fixture
def populated_engine():
    engine = Supervisor()
    for i in range(1, ENTITIES_COUNT+1):
        entity = engine.create_entity()
        name = Name(name=f'component_{i}', entity=entity)
        position = Position(x=i, y=i+2, entity=entity)
        engine.add_components(entity, [name, position])
    return engine


# TESTS
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


def test_remove_component(engine):
    entity = engine.create_entity()
    name = Name(name='test', entity=entity)
    engine.add_components(entity, name)

    assert len(engine.entities) == 1
    assert len(engine.components[name]) == 1
    assert len(entity.components[name]) == 1
    assert name in entity.components[name]

    engine.remove_components(name)

    assert len(engine.entities) == 1
    assert len(engine.components[name]) == 0
    assert len(entity.components[name]) == 0
    assert name not in entity.components[name]


def test_components_intersection(populated_engine):
    assert not populated_engine.get_components_intersection('FooBar')
    assert not populated_engine.get_components_intersection(
        ['FooBar', 'Name', 'Position']
    )

    for _ in range(0, 100):
        entity = populated_engine.create_entity()
        foobar = FooBar(foo=True, bar=False, entity=entity)
        populated_engine.add_components(entity, foobar)

    foobar_set = populated_engine.get_components_intersection('FooBar')
    assert len(foobar_set) == 100
    assert all(x.components['FooBar'] for x in foobar_set)

    for entity in list(populated_engine.entities.values())[:100]:
        foobar = FooBar(foo=True, bar=False, entity=entity)
        populated_engine.add_components(entity, foobar)

    foobar_set = populated_engine.get_components_intersection('FooBar')
    assert len(foobar_set) == 200

    foobar_name_set = populated_engine.get_components_intersection(
        ['FooBar', 'Name']
    )
    assert len(foobar_name_set) == 100
    assert all(
        x.components['FooBar'] and x.components['Name'] for x in foobar_name_set
    )


def test_system(populated_engine):
    populated_engine.add_system(NameSystem())
    populated_engine.execute_system(NameSystem)
    for entity in populated_engine.entities.values():
        assert all(x.name == TEST_NAME for x in entity.components['Name'])


def test_remove_system(engine):
    engine.add_system(NameSystem())
    assert len(engine.systems) == 1
    engine.remove_system(NameSystem)
    assert len(engine.systems) == 0


def test_systems_priority(engine):
    engine.add_system(NameSystem(priority=120))
    engine.add_system(PositionSystem(priority=10))

    assert isinstance(engine.systems[0], NameSystem)
    assert isinstance(engine.systems[1], PositionSystem)
