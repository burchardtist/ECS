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


@pytest.fixture
def one_orm():
    orm = ObjectRelationManager()

    person = SsnPerson()
    ssn = Ssn()
    orm.add(person, ssn)

    return orm, person, ssn


@pytest.fixture
def substitution_orm():
    orm = ObjectRelationManager()

    person = SsnPersonSubstitution()
    ssn = SsnSubstitution()
    orm.add(person, ssn)

    return orm, person, ssn


# Models
class IHouse:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person)


class House(IHouse):
    pass


class Cabin(IHouse):
    pass


class Cottage(IHouse):
    pass


class ManyRelationsHouse:
    def __init__(self):
        self.person_a: OneRelation = OneRelation(to_type=Person)
        self.person_b: OneRelation = OneRelation(to_type=Person)


class SubstitutionHouse:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person, substitution=True)


class Person:
    def __init__(self):
        self.houses: ManyRelation = ManyRelation(to_type=IHouse)


class SsnPerson:
    def __init__(self):
        self.ssn: OneRelation = OneRelation(to_type=Ssn)


class Ssn:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person)


class SsnPersonSubstitution:
    def __init__(self):
        self.ssn: OneRelation = OneRelation(to_type=Ssn, substitution=True)


class SsnSubstitution:
    def __init__(self):
        self.person: OneRelation = OneRelation(to_type=Person, substitution=True)


class Book:
    def __init__(self):
        self.authors: ManyRelation = ManyRelation(to_type=Author)


class Author:
    def __init__(self):
        self.books: ManyRelation = ManyRelation(to_type=Book)


# typing
TestObjects = Tuple[ObjectRelationManager, Person, List[House]]
TestPersonSsn = Tuple[ObjectRelationManager, SsnPerson, Ssn]
TestPersonSsnSubstitute = Tuple[
    ObjectRelationManager, SsnPersonSubstitution, SsnSubstitution
]
