from dataclasses import dataclass
from uuid import UUID

import pytest

from byt.ecs.component import IComponent
from byt.ecs.entity import Entity
from byt.ecs.system import ISystem
from byt.middleware.supervisor import Supervisor

ENTITIES_COUNT = 100
INTERSECTION_SAMPLE_COUNT = 10
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
            for position in engine.get_entity_components(entity)[Position]:
                position.x += 1
                position.y += 1


class NameSystem(ISystem):
    def process(self, engine, *args, **kwargs):
        name_entities = engine.get_components_intersection(Name)
        for entity in name_entities:
            for name in engine.get_entity_components(entity)[Name]:
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
        name = Name(name=f'component_{i}')
        position = Position(x=i, y=i+2)
        engine.add_components(entity, [name, position])
    return engine


# TESTS
def test_create_entity(engine):
    entity = engine.create_entity()
    assert isinstance(entity, Entity)
    assert isinstance(entity.id, UUID)
    assert len(engine.get_entity_components(entity)) == 0


def test_remove_entity(engine):
    entity = engine.create_entity()
    assert len(engine.entities) == 1
    engine.remove_entity(entity)
    assert len(engine.entities) == 0


def test_remove_entity_with_components(engine):
    name = Name(TEST_NAME)
    position = Position(x=1, y=10)
    entity = engine.create_entity()
    engine.add_components(entity, [name, position])

    assert len(engine.entities) == 1
    assert len(engine.get_entity_components(entity)) == len([name, position])

    engine.remove_entity(entity)
    assert len(engine.entities) == 0
    assert all([len(x) == 0 for x in engine.orm._objects.values()])


def test_add_and_remove_component(engine):
    entity = engine.create_entity()
    name = Name(name='test')
    engine.add_components(entity, name)

    name_components = engine.get_components(Name)
    entity_components = engine.get_entity_components(entity)
    assert len(engine.entities) == 1
    assert len(name_components) == 1
    assert len(entity_components) == 1
    assert name in name_components
    assert name in entity_components[Name]

    engine.remove_components(name)
    name_components = engine.get_components(Name)
    entity_components = engine.get_entity_components(entity)
    assert len(engine.entities) == 1
    assert len(name_components) == 0
    assert len(entity_components) == 0
    assert name not in name_components
    assert not entity_components


def test_components_intersection(engine):
    assert not engine.get_components_intersection(FooBar)
    assert not engine.get_components_intersection([FooBar, Name, Position])

    new_entities = list()
    for _ in range(INTERSECTION_SAMPLE_COUNT):
        entity = engine.create_entity()
        new_entities.append(entity)
        foobar = FooBar(foo=True, bar=False)
        engine.add_components(entity, foobar)

    foobar_set = engine.get_components_intersection(FooBar)
    assert len(foobar_set) == INTERSECTION_SAMPLE_COUNT

    for entity in new_entities:
        components = engine.get_entity_components(entity)
        foobar_component = components[FooBar].pop()
        assert len(components) == 1
        assert engine.get_component_entity(foobar_component) in foobar_set


def test_components_intersection_many(populated_engine):
    engine = populated_engine
    all_component_types = [Name, Position, FooBar]

    name_components = engine.get_components_intersection(Name)
    assert len(name_components) == ENTITIES_COUNT

    foobar_components = engine.get_components_intersection(FooBar)
    assert len(foobar_components) == 0

    name_foobar_components = engine.get_components_intersection([Name, FooBar])
    assert len(name_foobar_components) == 0

    part_of_entities = list(engine.entities.values())[:INTERSECTION_SAMPLE_COUNT]
    other_entities = list(engine.entities.values())[INTERSECTION_SAMPLE_COUNT:]
    for entity in part_of_entities:
        foobar = FooBar(foo=True, bar=False)
        engine.add_components(entity, foobar)

    foobar_name_components = engine.get_components_intersection([FooBar, Name])
    assert len(foobar_name_components) == INTERSECTION_SAMPLE_COUNT

    all_components = engine.get_components_intersection(all_component_types)
    assert len(all_components) == INTERSECTION_SAMPLE_COUNT

    name_position_components = engine.get_components_intersection([Name, Position])
    assert len(name_position_components) == ENTITIES_COUNT

    for entity in part_of_entities:
        components = engine.get_entity_components(entity)
        assert len(components) == len(all_component_types)
        name_component = components[Name].pop()
        name_entity = engine.get_component_entity(name_component)
        position_component = components[Position].pop()
        position_entity = engine.get_component_entity(position_component)
        assert name_entity in name_position_components
        assert name_entity in foobar_name_components
        assert position_entity in name_position_components

    for entity in other_entities:
        components = engine.get_entity_components(entity)
        assert FooBar not in components
        assert Name in components
        assert Position in components


def test_system(populated_engine):
    engine = populated_engine

    engine.add_system(NameSystem())
    engine.execute_system(NameSystem)
    components = engine.get_components(Name)
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
