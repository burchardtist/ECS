from typing import List, Tuple

import pytest

from byt.object_relations.control import ObjectRelationManager
from byt.object_relations.error import ManySameRelationsError, \
    MissingRelationError, SubstitutionNotAllowedError
from byt.object_relations.relations import ManyRelation, OneRelation

SAMPLE_SIZE = 50


# FIXTURES
@pytest.fixture
def orm():
    return ObjectRelationManager()


@pytest.fixture
def populated_orm():
    orm = ObjectRelationManager()

    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = House()
        houses_list.append(house)
        orm.add(person, house)

    return orm, person, houses_list


@pytest.fixture
def many_orm():
    orm = ObjectRelationManager()

    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = House()
        cabin = Cabin()
        houses_list.append(house)
        houses_list.append(cabin)
        orm.add(person, house)
        orm.add(person, cabin)

    return orm, person, houses_list


@pytest.fixture
def substitution_relation_orm():
    orm = ObjectRelationManager()

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


class House(IHouse):
    pass


class Cabin(IHouse):
    pass


class Cottage(IHouse):
    pass


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


TestObjects = Tuple[ObjectRelationManager, Person, List[House]]


# TESTS
def test_unique_id():
    ids = {Person().houses.id for _ in range(SAMPLE_SIZE)}
    assert len(ids) == SAMPLE_SIZE


def test_get_relation(orm):
    person = Person()
    house = House()

    assert orm.get_relation(person.houses) is None

    orm.add(person, house)
    houses = list(orm.get_relation(person.houses))
    assert len(houses) == 1
    assert houses[0] is house
    house_person = orm.get_relation(house.person)
    assert house_person
    assert house_person is person

    orm.remove(person, house)
    assert len(orm.get_relation(person.houses)) == 0
    assert not orm.get_relation(house.person)


def test_get_type(orm):
    person = Person()
    house = House()

    assert orm.get_relation(person.houses) is None

    orm.add(person, house)
    person_list = list(orm.get_type(Person))
    house_list = list(orm.get_type(House))
    assert len(person_list) == 1
    assert person_list[0] is person
    assert len(house_list) == 1
    assert house_list[0] is house

    orm.remove(person, house)
    assert len(orm.get_type(Person)) == 0
    assert len(orm.get_type(House)) == 0


def test_add(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    assert len(orm.get_relation(person.houses)) == SAMPLE_SIZE
    assert all([orm.get_relation(house.person) is person for house in houses])


def test_remove(populated_orm: TestObjects):
    orm, person, houses = populated_orm

    house = houses[0]
    assert orm.get_relation(house.person) is person

    orm.remove(person, house)
    assert orm.get_relation(house.person) is None
    assert len(orm.get_relation(person.houses)) == SAMPLE_SIZE - 1
    assert house not in orm.get_relation(person.houses)


def test_multiple_relations(orm: ObjectRelationManager):
    person = Person()
    house = ManyRelationsHouse()
    with pytest.raises(ManySameRelationsError):
        orm.add(person, house)


def _test_substitution(orm, house, houses, person, another_person):
    assert all([orm.get_relation(house.person) is person for house in houses])
    assert house not in orm.get_relation(person.houses)
    assert len(orm.get_relation(person.houses)) == SAMPLE_SIZE - 1
    assert house in orm.get_relation(another_person.houses)
    assert orm.get_relation(house.person) is another_person
    assert orm.get_relation(house.person) is not person


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

    another_house = House()
    another_person = Person()

    with pytest.raises(MissingRelationError):
        orm.remove(houses[0], another_person)

    with pytest.raises(MissingRelationError):
        orm.remove(another_house, person)


def test_add_many_types(many_orm):
    orm, person, houses = many_orm
    total_size = SAMPLE_SIZE * len([House, Cabin])

    assert len(houses) == total_size
    assert not [x for x in houses if isinstance(x, Cottage)]

    cottage = Cottage()
    orm.add(person, cottage)
    person_houses = orm.get_relation(person.houses)

    assert len(person_houses) == total_size + 1
    assert len([x for x in person_houses if isinstance(x, Cottage)]) == 1


def test_get_many_types(many_orm):
    orm, person, houses = many_orm

    person_houses = orm.get_relation(person.houses)
    cabins = [x for x in person_houses if isinstance(x, Cabin)]
    houses = [x for x in person_houses if isinstance(x, House)]

    assert all([orm.get_relation(house.person) is person for house in houses])
    assert len(cabins) == SAMPLE_SIZE
    assert len(houses) == SAMPLE_SIZE
    assert len(person_houses) == len(cabins) + len(houses)


def test_remove_many_types(many_orm):
    orm, person, houses = many_orm

    cabins = [x for x in houses if isinstance(x, Cabin)]

    for cabin in cabins:
        orm.remove(person, cabin)

    person_houses = orm.get_relation(person.houses)
    assert not [x for x in person_houses if isinstance(x, Cabin)]
    assert len([x for x in person_houses if isinstance(x, House)]) == SAMPLE_SIZE
    assert len(person_houses) == SAMPLE_SIZE
