from typing import List, Tuple

import pytest

from byt.object_relations.control import ObjectRelation
from byt.object_relations.error import ManySameRelationsError, \
    MissingRelationError, SubstitutionNotAllowedError
from byt.object_relations.relations import ManyRelation, OneRelation

SAMPLE_SIZE = 50


# FIXTURES
@pytest.fixture
def orm():
    return ObjectRelation()


@pytest.fixture
def populated_orm():
    orm = ObjectRelation()

    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = IHouse()
        houses_list.append(house)
        orm.add(person, house)

    return orm, person, houses_list


@pytest.fixture
def substitution_relation_orm():
    orm = ObjectRelation()

    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = SubstitutionHouse()
        houses_list.append(house)
        orm.add(person, house)

    return orm, person, houses_list


# TEST MODELS
class IHouse:
    person: OneRelation

    def __init__(self):
        self.person = OneRelation(to_type=Person)


class ManyRelationsHouse:
    person_a: OneRelation
    person_b: OneRelation

    def __init__(self):
        self.person_a = OneRelation(to_type=Person)
        self.person_b = OneRelation(to_type=Person)


class SubstitutionHouse:
    person: OneRelation

    def __init__(self):
        self.person = OneRelation(to_type=Person, substitution=True)


class Person:
    houses: ManyRelation

    def __init__(self):
        self.houses = ManyRelation(to_type=IHouse)


TestObjects = Tuple[ObjectRelation, Person, List[IHouse]]


# TESTS
def test_unique_id():
    ids = {Person().houses.id for _ in range(SAMPLE_SIZE)}
    assert len(ids) == SAMPLE_SIZE


def test_get(orm):
    person = Person()
    house = IHouse()

    assert orm.get(person.houses) is None
    orm.add(person, house)
    assert len(orm.get(person.houses)) == 1


def test_add(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    assert len(orm.get(person.houses)) == SAMPLE_SIZE
    assert all([orm.get(house.person) is person for house in houses])


def test_remove(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    house = houses[0]
    assert orm.get(house.person) is person

    orm.remove(person, house)
    assert orm.get(house.person) is None
    assert len(orm.get(person.houses)) == SAMPLE_SIZE - 1
    assert house not in orm.get(person.houses)


def test_multiple_relations(orm: ObjectRelation):
    person = Person()
    house = ManyRelationsHouse()
    with pytest.raises(ManySameRelationsError):
        orm.add(person, house)


def _test_substitution(orm, house, houses, person, another_person):
    assert all([orm.get(house.person) is person for house in houses])
    assert house not in orm.get(person.houses)
    assert len(orm.get(person.houses)) == SAMPLE_SIZE - 1
    assert house in orm.get(another_person.houses)
    assert orm.get(house.person) is another_person
    assert orm.get(house.person) is not person


def test_substitution_relation(substitution_relation_orm: TestObjects):
    orm, person, houses = substitution_relation_orm

    another_person = Person()
    house = houses.pop()

    orm.add(another_person, house)
    _test_substitution(orm, house, houses, person, another_person)


def test_substitution_relation_reverted(substitution_relation_orm: TestObjects):
    orm, person, houses = substitution_relation_orm

    another_person = Person()
    house = houses.pop()

    orm.add(house, another_person)
    _test_substitution(orm, house, houses, person, another_person)


def test_substitution_not_allowed_relation(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    another_person = Person()
    house = houses.pop()

    with pytest.raises(SubstitutionNotAllowedError):
        orm.add(another_person, house)


def test_missing_relation(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    another_house = IHouse()
    another_person = Person()

    with pytest.raises(MissingRelationError):
        orm.remove(houses[0], another_person)

    with pytest.raises(MissingRelationError):
        orm.remove(another_house, person)
