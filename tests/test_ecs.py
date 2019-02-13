from dataclasses import dataclass
from uuid import UUID

import pytest

from byt.ecs.component import IComponent
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.supervisor import Supervisor

ENTITIES_COUNT = 5000
TEST_NAME = 'NameSystemTest'


# COMPONENTS
@dataclass(eq=False)
class Name(IComponent):
    name: str


@dataclass(eq=False)
class Position(IComponent):
    x: int
    y: int


@dataclass(eq=False)
class FooBar(IComponent):
    foo: bool
    bar: bool


# SYSTEMS
class PositionSystem(ISystem):
    def process(self, engine, *args, **kwargs):
        position_entities = engine.get_components_intersection(Position)
        for entity in position_entities:
            for position in entity.components.get_group(Position):
                position.x += 1
                position.y += 1


class NameSystem(ISystem):
    def process(self, engine, *args, **kwargs):
        name_entities = engine.get_components_intersection(Name)
        for entity in name_entities:
            for name in entity.components.get_group(Name):
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
    assert not entity.components.get_all()


def test_populated_supervisor(populated_engine):
    assert len(populated_engine.entities) == ENTITIES_COUNT
    for _, value in populated_engine.component_manager.get_all():
        assert len(value) == ENTITIES_COUNT
    assert populated_engine.component_manager.group_len(FooBar) == 0

    entity_ids = [x for x in populated_engine.entities]
    for entity_id in entity_ids:
        entity = populated_engine.get_entity(entity_id)
        populated_engine.remove_entity(entity)

    assert len(populated_engine.entities) == 0
    for _, value in populated_engine.component_manager.get_all():
        assert len(value) == 0


def test_remove_component(engine):
    entity = engine.create_entity()
    name = Name(name='test', entity=entity)
    engine.add_components(entity, name)

    assert len(engine.entities) == 1
    assert engine.component_manager.group_len(name) == 1
    assert entity.components.group_len(name) == 1
    assert name in list(entity.components.get_group(name))
    engine.remove_components(name)

    assert len(engine.entities) == 1
    assert engine.component_manager.group_len(name) == 0
    assert entity.components.group_len(name) == 0
    assert name not in list(entity.components.get_group(name))


def test_components_intersection(populated_engine):
    assert not populated_engine.get_components_intersection(FooBar)
    assert not populated_engine.get_components_intersection(
        [FooBar, Name, Position]
    )

    for _ in range(0, 100):
        entity = populated_engine.create_entity()
        foobar = FooBar(foo=True, bar=False, entity=entity)
        populated_engine.add_components(entity, foobar)

    foobar_set = populated_engine.get_components_intersection(FooBar)
    assert len(foobar_set) == 100
    assert all(list(x.components.get_group(FooBar)) for x in foobar_set)

    for entity in list(populated_engine.entities.values())[:100]:
        foobar = FooBar(foo=True, bar=False, entity=entity)
        populated_engine.add_components(entity, foobar)

    foobar_set = populated_engine.get_components_intersection(FooBar)
    assert len(foobar_set) == 200

    foobar_name_set = populated_engine.get_components_intersection(
        [FooBar, Name]
    )
    assert len(foobar_name_set) == 100

    assert all(
        x.components.group_len(FooBar) == 1 and x.components.group_len(Name) == 1
        for x in foobar_name_set
    )


def test_system(populated_engine):
    populated_engine.add_system(NameSystem())
    populated_engine.execute_system(NameSystem)
    for entity in populated_engine.entities.values():
        components = list(entity.components.get_group(Name))
        assert all(x.name == TEST_NAME for x in components)


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
