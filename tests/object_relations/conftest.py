from typing import List, Tuple

import pytest

from byt.object_relations.control import ObjectRelationManager
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
def substitution_relation_orm():
    orm = ObjectRelationManager()

    person = Person()
    houses_list = list()

    for _ in range(SAMPLE_SIZE):
        house = SubstitutionHouse()
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


# Models
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


# typing
TestObjects = Tuple[ObjectRelationManager, Person, List[House]]
